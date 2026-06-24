from django.core.management.base import BaseCommand
from matching.models import Question


class Command(BaseCommand):
    help = '양자택일 질문 시드 데이터 삽입'

    def handle(self, *args, **kwargs):
        # (A, B, match_type, weight)
        questions = [
            ('넷플릭스', '유튜브', 'similar', 1.0),
            ('한식', '양식', 'similar', 1.0),
            ('소주', '맥주', 'similar', 1.2),
            ('블랙', '화이트', 'neutral', 0.5),
            ('강아지', '고양이', 'similar', 1.0),
            ('세단', 'SUV', 'neutral', 0.7),
            ('생머리', '파마', 'neutral', 0.5),
            ('바다', '산', 'similar', 1.0),
            ('고층', '저층', 'neutral', 0.7),
            ('고기', '해물', 'similar', 1.0),
            ('밥', '면', 'similar', 0.8),
            ('전화', '카톡', 'complement', 1.0),   # 연락방식 - 다를 때 보완
            ('아침형', '저녁형', 'similar', 1.2),   # 생활패턴 - 중요
            ('여름', '겨울', 'similar', 0.8),
            ('게임', '운동', 'complement', 0.8),
            ('참외', '딸기', 'neutral', 0.4),
            ('초콜릿', '젤리', 'neutral', 0.4),
            ('물냉면', '비빔냉면', 'neutral', 0.5),
            ('붕어빵 머리', '붕어빵 꼬리', 'neutral', 0.3),
            ('치킨 다리', '치킨 날개', 'neutral', 0.3),
            ('부먹', '찍먹', 'neutral', 0.5),
        ]

        Question.objects.all().delete()  # 기존 질문 초기화
        for i, (a, b, mtype, w) in enumerate(questions):
            Question.objects.create(
                option_a=a, option_b=b,
                match_type=mtype, weight=w, order=i
            )

        self.stdout.write(self.style.SUCCESS(f'{len(questions)}개 질문 생성 완료!'))
