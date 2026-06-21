from .models import Answer, Question


def get_answer_map(user):
    """ {question_id: set(choice_id, ...)} 형태로 변환 """
    result = {}
    for ans in Answer.objects.filter(user=user):
        result.setdefault(ans.question_id, set()).add(ans.choice_id)
    return result


def calculate_similarity(user_a, user_b, question_cache=None):
    """
    두 유저의 유사도를 0~100 점수로 반환.
    match_type(similar/complement/neutral)과
    유저의 match_preference를 반영.
    """
    a_answers = get_answer_map(user_a)
    b_answers = get_answer_map(user_b)

    # 둘 다 답변한 공통 질문만 비교 (꼬리질문 스킵 처리)
    common_q_ids = set(a_answers) & set(b_answers)
    if not common_q_ids:
        return 0.0

    # 질문 정보 캐싱 (매번 DB 조회 방지)
    if question_cache is None:
        question_cache = {q.id: q for q in Question.objects.all()}

    total_weight = 0.0
    match_score = 0.0

    # 두 유저의 선호도가 모두 complement면 "다른 사람"을 더 높게 평가
    both_complement = (
        user_a.match_preference == 'complement'
        and user_b.match_preference == 'complement'
    )

    for qid in common_q_ids:
        q = question_cache.get(qid)
        if not q:
            continue

        a_set = a_answers[qid]
        b_set = b_answers[qid]

        # 1) 기본 일치도 계산
        if q.q_type == 'single':
            base_sim = 1.0 if a_set == b_set else 0.0
        else:  # multi → 자카드 유사도
            base_sim = len(a_set & b_set) / len(a_set | b_set)

        # 2) match_type 반영
        if q.match_type == 'complement':
            # 다를수록 좋은 질문 → 점수 반전
            sim = 1.0 - base_sim
        else:  # similar, neutral → 같을수록 좋음
            sim = base_sim

        # 3) 유저 선호도 반영 (둘 다 complement면 다른 점을 가산)
        weight = q.weight
        if both_complement and q.match_type == 'complement':
            weight *= 1.5   # 보완 매칭 선호 시 가중치 강화

        match_score += sim * weight
        total_weight += weight

    if total_weight == 0:
        return 0.0

    return round(match_score / total_weight * 100, 1)
