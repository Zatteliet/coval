from coval.conll import reader
from coval.conll import util
from coval.eval import evaluator


key_file = "gold.conll"
sys_file = "pred.conll"
NP_only = False
remove_nested = False
keep_singletons = True
min_span = False


def main():
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
    evaluate(metrics)


def evaluate(metrics):
    doc_coref_infos = reader.get_coref_infos(
        key_file, sys_file, NP_only, remove_nested, keep_singletons, min_span
    )

    conll = 0
    conll_subparts_num = 0

    for name, metric in metrics:
        recall, precision, f1 = evaluator.evaluate_documents(
            doc_coref_infos, metric, beta=1
        )
        if name in ["muc", "bcub", "ceafe"]:
            conll += f1
            conll_subparts_num += 1

        print(
            name.ljust(10),
            "Recall: %.2f" % (recall * 100),
            " Precision: %.2f" % (precision * 100),
            " F1: %.2f" % (f1 * 100),
        )

    if conll_subparts_num == 3:
        conll = (conll / 3) * 100
        print("CoNLL score: %.2f" % conll)


if __name__ == "__main__":
    main()
