import argparse
from subprocess import Popen, PIPE, STDOUT

import numpy as np
from numpy import apply_along_axis as npa

class Handler:
    @classmethod
    def scoring(cls, instance):
        from app import Session
        from app.controller import Assignment
        from app.controller import Submission
        process = Popen(['python', 'app/lib/handler.py',
                        Submission.get_file_path(instance.file),
                        Assignment.get_file_path(instance.assignment.label),
                        str(instance.assignment.cate)],
                        stdout=PIPE,
                        stderr=STDOUT)
        result, *_ = process.communicate()
        print (result)
        instance.state = 'done'
        instance.result = 'done'
        instance.score = float(result.decode('utf-8'))
        Session.commit()

    @classmethod
    def evaluate(cls, filename, labelname, cate):
        from differ import Differ
        from metric import Metric
        metric = Metric.__subclasses__()[cate]
        differ = Differ(filename, labelname, metric)
        print (differ.score())

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename",
                        help="submission file name",
                        type=str)
    parser.add_argument("labelname",
                        help="assignment label name",
                        type=str)
    parser.add_argument("cate",
                        help="assignment category",
                        type=int)
    args = parser.parse_args()
    Handler.evaluate(args.filename, args.labelname, int(args.cate))
