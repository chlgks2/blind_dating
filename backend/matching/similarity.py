from .models import Answer, Question


def get_answer_map(user):
    """ {question_id: 'A' or 'B'} """
    return {
        a.question_id: a.selected
        for a in Answer.objects.filter(user=user)
    }


def calculate_similarity(user_a, user_b, question_cache=None):
    a_answers = get_answer_map(user_a)
    b_answers = get_answer_map(user_b)

    common_q_ids = set(a_answers) & set(b_answers)
    if not common_q_ids:
        return 0.0

    if question_cache is None:
        question_cache = {q.id: q for q in Question.objects.all()}

    total_weight = 0.0
    match_score = 0.0

    both_complement = (
        user_a.match_preference == 'complement'
        and user_b.match_preference == 'complement'
    )

    for qid in common_q_ids:
        q = question_cache.get(qid)
        if not q:
            continue

        # 같은 선택이면 1, 다르면 0
        same = (a_answers[qid] == b_answers[qid])
        base_sim = 1.0 if same else 0.0

        # match_type 반영
        if q.match_type == 'complement':
            sim = 1.0 - base_sim   # 다를수록 좋음
        else:
            sim = base_sim         # 같을수록 좋음

        weight = q.weight
        if both_complement and q.match_type == 'complement':
            weight *= 1.5

        match_score += sim * weight
        total_weight += weight

    if total_weight == 0:
        return 0.0
    return round(match_score / total_weight * 100, 1)
