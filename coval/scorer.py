from tabulate import tabulate

from coval.conll import reader, util
from coval.eval import evaluator


def score(
    key_file,
    sys_file,
    *,
    np_only=False,
    remove_nested=False,
    keep_singletons=True,
    min_span=False,
):
    if min_span:
        has_gold_parse = util.check_gold_parse_annotation(key_file)
        if not has_gold_parse:
            util.parse_key_file(key_file)
            key_file = key_file + ".parsed"

    # Remove option to only compute some metrics and some others.
    metrics = [
        ("mentions", evaluator.mentions),
        ("muc", evaluator.muc),
        ("bcub", evaluator.b_cubed),
        ("ceafe", evaluator.ceafe),
        ("lea", evaluator.lea),
    ]

    doc_coref_infos = reader.get_coref_infos(
        key_file, sys_file, np_only, remove_nested, keep_singletons, min_span
    )

    conll = 0
    conll_subparts_num = 0

    scores = []
    for name, metric in metrics:
        recall, precision, f1 = evaluator.evaluate_documents(
            doc_coref_infos, metric, beta=1
        )
        scores.append([name, recall, precision, f1])
        if name in ["muc", "bcub", "ceafe"]:
            conll += f1
            conll_subparts_num += 1
    headers = ["name", "recall", "precision", "f1"]
    print(tabulate(scores, headers=headers, tablefmt="fancy_grid"))

    if conll_subparts_num == 3:
        conll = (conll / 3) * 100
        print(tabulate([["ConLL score", conll]], tablefmt="fancy_grid"))