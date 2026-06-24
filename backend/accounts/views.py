from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

from .serializers import SignupSerializer, UserProfileSerializer

from .models import AIJob
from .s3_utils import upload_fileobj
from .s3_utils import upload_bytes


User = get_user_model()


class SignupAPIView(generics.CreateAPIView):
    """회원가입 - 누구나 접근 가능"""
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]


class MyProfileAPIView(APIView):
    """내 정보 조회 - 로그인 필요 (request.user 사용)"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)


class AIJobCreateAPIView(APIView):
    """
    [유저용] 사진 업로드 + 스타일 선택 → 작업 등록
    form-data: image(파일), style(문자열)
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        image_file = request.FILES.get('image')
        style = request.data.get('style')

        if not image_file:
            return Response({'error': '이미지 필요'}, status=400)
        if style not in dict(AIJob.STYLE_CHOICES):
            return Response({'error': '올바른 스타일 필요'}, status=400)

        # S3에 원본 업로드
        original_url, _ = upload_fileobj(image_file, folder='originals')

        # 작업 등록 (pending)
        job = AIJob.objects.create(
            user=user, style=style,
            original_url=original_url, status='pending'
        )

        return Response({
            'job_id': job.id,
            'status': job.status,
            'message': '변환 작업이 등록되었습니다. 잠시만 기다려주세요.',
        }, status=201)


class AIJobStatusAPIView(APIView):
    """[유저용] 내 작업 상태 확인 (폴링)"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, job_id):
        try:
            job = AIJob.objects.get(id=job_id, user=request.user)
        except AIJob.DoesNotExist:
            return Response({'error': '작업을 찾을 수 없음'}, status=404)

        return Response({
            'job_id': job.id,
            'status': job.status,
            'generated_url': job.generated_url,
            'error': job.error_message,
        })


# ===== GPU 워커가 사용하는 API =====

class NextJobAPIView(APIView):
    """[워커용] 대기중인 작업 1개 가져가기"""
    permission_classes = [permissions.AllowAny]  # 워커용 (간단히. 나중에 비밀키 인증)

    def get(self, request):
        job = AIJob.objects.filter(status='pending').first()
        if not job:
            return Response({'job': None})

        # 중복 처리 방지: processing으로 변경
        job.status = 'processing'
        job.save()

        return Response({'job': {
            'job_id': job.id,
            'style': job.style,
            'original_url': job.original_url,
        }})


class CompleteJobAPIView(APIView):
    """[워커용] 작업 완료 통보"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        job_id = request.data.get('job_id')
        generated_url = request.data.get('generated_url')
        error = request.data.get('error')

        try:
            job = AIJob.objects.get(id=job_id)
        except AIJob.DoesNotExist:
            return Response({'error': '작업 없음'}, status=404)

        if error:
            job.status = 'failed'
            job.error_message = error
        else:
            job.status = 'done'
            job.generated_url = generated_url
        job.save()

        return Response({'message': '상태 업데이트 완료'})


class CompleteUploadJobAPIView(APIView):
    """[워커용] 결과 이미지 파일을 받아서 S3 업로드 + 완료 처리"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        job_id = request.data.get('job_id')
        result_file = request.FILES.get('result')

        try:
            job = AIJob.objects.get(id=job_id)
        except AIJob.DoesNotExist:
            return Response({'error': '작업 없음'}, status=404)

        # 결과를 S3에 업로드
        generated_url, _ = upload_bytes(
            result_file.read(), folder='generated', ext='png'
        )

        job.generated_url = generated_url
        job.status = 'done'
        job.save()

        job.user.profile_image_url = generated_url
        job.user.save()

        return Response({'message': '완료', 'generated_url': generated_url})
