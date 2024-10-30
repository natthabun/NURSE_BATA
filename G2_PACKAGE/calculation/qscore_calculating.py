def cal_qs(record):
    phred_scores = record.letter_annotations["phred_quality"]
    return sum(phred_scores) / len(phred_scores) if phred_scores else 0 