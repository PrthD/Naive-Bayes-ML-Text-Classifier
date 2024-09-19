"""
--------------------------------------------
Name: Parth Dadhania
SID: 1722612
CCID: pdadhani
AnonID: 1000330704
CMPUT 274, Fall 2022
Assessment: Assignment #1: OO Classifier
--------------------------------------------
"""

import sys
import copy     # for deepcopy()
import re       # for method is_alnum() to remove non-alphanumeric characters

Debug = False   # Sometimes, print for debugging.  Overridable on command line.
InputFilename = "file.input.txt"
TargetWords = [
        'outside', 'today', 'weather', 'raining', 'nice', 'rain', 'snow',
        'day', 'winter', 'cold', 'warm', 'snowing', 'out', 'hope', 'boots',
        'sunny', 'windy', 'coming', 'perfect', 'need', 'sun', 'on', 'was',
        '-40', 'jackets', 'wish', 'fog', 'pretty', 'summer'
        ]


def open_file(filename=InputFilename):
    try:
        f = open(filename, "r")
        return(f)
    except FileNotFoundError:
        # FileNotFoundError is subclass of OSError
        if Debug:
            print("File Not Found")
        return(sys.stdin)
    except OSError:
        if Debug:
            print("Other OS Error")
        return(sys.stdin)


def safe_input(f=None, prompt=""):
    try:
        # Case:  Stdin
        if f is sys.stdin or f is None:
            line = input(prompt)
        # Case:  From file
        else:
            assert not (f is None)
            assert (f is not None)
            line = f.readline()
            if Debug:
                print("readline: ", line, end='')
            if line == "":  # Check EOF before strip()
                if Debug:
                    print("EOF")
                return("", False)
        return(line.strip(), True)
    except EOFError:
        return("", False)


class C274:
    def __init__(self):
        self.type = str(self.__class__)
        return

    def __str__(self):
        return(self.type)

    def __repr__(self):
        s = "<%d> %s" % (id(self), self.type)
        return(s)


class ClassifyByTarget(C274):
    def __init__(self, lw=[]):
        super().__init__()      # Call superclass
        # self.type = str(self.__class__)
        self.allWords = 0
        self.theCount = 0
        self.nonTarget = []
        self.set_target_words(lw)
        self.initTF()
        return

    def initTF(self):
        self.TP = 0
        self.FP = 0
        self.TN = 0
        self.FN = 0
        return

    # FIXME:  Incomplete.  Finish get_TF() and other getters/setters.
    def get_TF(self):
        return(self.TP, self.FP, self.TN, self.FN)

    # TODO: Could use Use Python properties
    #     https://www.python-course.eu/python3_properties.php
    def set_target_words(self, lw):
        # Could also do self.targetWords = lw.copy().  Thanks, TA Jason Cannon
        self.targetWords = copy.deepcopy(lw)
        return

    def get_target_words(self):
        return(self.targetWords)

    def get_allWords(self):
        return(self.allWords)

    def incr_allWords(self):
        self.allWords += 1
        return

    def get_theCount(self):
        return(self.theCount)

    def incr_theCount(self):
        self.theCount += 1
        return

    def get_nonTarget(self):
        return(self.nonTarget)

    def add_nonTarget(self, w):
        self.nonTarget.append(w)
        return

    def print_config(self, printSorted=True):
        print("-------- Print Config --------")
        ln = len(self.get_target_words())
        print("TargetWords (%d): " % ln, end='')
        if printSorted:
            print(sorted(self.get_target_words()))
        else:
            print(self.get_target_words())
        return

    def print_run_info(self, printSorted=True):
        print("-------- Print Run Info --------")
        print("All words:%3s. " % self.get_allWords(), end='')
        print(" Target words:%3s" % self.get_theCount())
        print("Non-Target words (%d): " % len(self.get_nonTarget()), end='')
        if printSorted:
            print(sorted(self.get_nonTarget()))
        else:
            print(self.get_nonTarget())
        return

    def print_confusion_matrix(self, targetLabel, doKey=False, tag=""):
        assert (self.TP + self.TP + self.FP + self.TN) > 0
        print(tag+"-------- Confusion Matrix --------")
        print(tag+"%10s | %13s" % ('Predict', 'Label'))
        print(tag+"-----------+----------------------")
        print(tag+"%10s | %10s %10s" % (' ', targetLabel, 'not'))
        if doKey:
            print(tag+"%10s | %10s %10s" % ('', 'TP   ', 'FP   '))
        print(tag+"%10s | %10d %10d" % (targetLabel, self.TP, self.FP))
        if doKey:
            print(tag+"%10s | %10s %10s" % ('', 'FN   ', 'TN   '))
        print(tag+"%10s | %10d %10d" % ('not', self.FN, self.TN))
        return

    def eval_training_set(self, tset, targetLabel, lines=True):
        print("-------- Evaluate Training Set --------")
        self.initTF()
        # zip is good for parallel arrays and iteration
        z = zip(tset.get_instances(), tset.get_lines())
        for ti, w in z:
            lb = ti.get_label()
            cl = ti.get_class()
            if lb == targetLabel:
                if cl:
                    self.TP += 1
                    outcome = "TP"
                else:
                    self.FN += 1
                    outcome = "FN"
            else:
                if cl:
                    self.FP += 1
                    outcome = "FP"
                else:
                    self.TN += 1
                    outcome = "TN"
            explain = ti.get_explain()
            # Format nice output
            if lines:
                w = ' '.join(w.split())
            else:
                w = ' '.join(ti.get_words())
                w = lb + " " + w

            # TW = testing bag of words words (kinda arbitrary)
            print("TW %s: ( %10s) %s" % (outcome, explain, w))
            if Debug:
                print("-->", ti.get_words())
        self.print_confusion_matrix(targetLabel)
        return

    def classify_by_words(self, ti, update=False, tlabel="last"):
        inClass = False
        evidence = ''
        lw = ti.get_words()
        for w in lw:
            if update:
                self.incr_allWords()
            if w in self.get_target_words():    # FIXME Write predicate
                inClass = True
                if update:
                    self.incr_theCount()
                if evidence == '':
                    evidence = w            # FIXME Use first word, but change
            elif w != '':
                if update and (w not in self.get_nonTarget()):
                    self.add_nonTarget(w)
        if evidence == '':
            evidence = '#negative'
        if update:
            ti.set_class(inClass, tlabel, evidence)
        return(inClass, evidence)

    # Could use a decorator, but not now
    def classify(self, ti, update=False, tlabel="last"):
        cl, e = self.classify_by_words(ti, update, tlabel)
        return(cl, e)

    def classify_all(self, ts, update=True, tlabel="classify_all"):
        for ti in ts.get_instances():
            cl, e = self.classify(ti, update=update, tlabel=tlabel)
        return


class ClassifyByTopN(ClassifyByTarget):
    def __init__(self, lw=[]):
        super().__init__(lw)
        return

    def target_top_n(self, tset, num=5, label=''):
        new_trgt_words = []
        # appending those words whose label matches the
        # input argument 'label'
        for instance in tset.get_instances():
            lbl = instance.get_label()
            if lbl == label:
                new_trgt_words.extend(instance.get_words())
        freq_dict = {}
        # frequency calculation (using dictionary) of those words
        # whose label matches the input argut 'label'
        for word_key in new_trgt_words:
            if word_key not in freq_dict.keys():
                freq_dict[word_key] = 1
            else:
                freq_dict[word_key] += 1
        topN_lst = []
        counter = 1
        dict_key = sorted(freq_dict, key=freq_dict.get, reverse=True)
        # setting new target words with those 'num' words which has the
        # highest frequencies in freq_dict dictionary
        for key in dict_key:
            if (counter > num) and (freq_dict[topN_lst[-1]] == freq_dict[key]):
                topN_lst.append(key)
                counter += 1
            elif counter <= num:
                topN_lst.append(key)
                counter += 1
            else:
                break
        self.set_target_words(topN_lst)
        return


class TrainingInstance(C274):
    def __init__(self):
        super().__init__()              # Call superclass
        # self.type = str(self.__class__)
        self.inst = dict()
        # FIXME:  Get rid of dict, and use attributes
        self.inst["label"] = "N/A"      # Class, given by oracle
        self.inst["words"] = []         # Bag of words
        self.inst["class"] = ""         # Class, by classifier
        self.inst["explain"] = ""       # Explanation for classification
        self.inst["experiments"] = dict()   # Previous classifier runs
        return

    def preprocess_words(self, mode=''):
        """ This method processes the input argument given at the invocation
        to run the program, checks if the proper arguments are used and whether
        the usage is correct. The function also manages the different modes of
        the program.

        Arguments:
            mode='': Optional input argument for the different modes this
                     program can run using.

        Returns:
            1: The function will only return '1' when the 'mode' argument used
               in command line doesn't match any of the correct argument forms.
        """
        # preprocessing input according to the mode provided by the
        # input argument 'mode'
        inp = self.input_text_lowercase(self.inst["words"])
        if mode == '':
            out1 = self.is_alnum(inp)
            out2 = self.remove_num(out1)
            processed_words = self.stop_word_process(out2)
        elif mode == 'keep-digits':
            out1 = self.is_alnum(inp)
            processed_words = self.stop_word_process(out1)
        elif mode == 'keep-stops':
            out1 = self.is_alnum(inp)
            processed_words = self.remove_num(out1)
        elif mode == 'keep-symbols':
            out1 = self.remove_num(inp)
            processed_words = self.stop_word_process(out1)
        else:
            print('ERROR: Optional command line argument does not match.\n')
            print('The proper usage of program is:')
            print('           "python3 preprocess.py <mode>"         ')
            print('\nHere mode can STRICTLY be either empty or one of the')
            print('following: "keep-digits", "keep-stops" or "keep-symbols".')
            sys.exit('1')
        # setting the attribute 'words' as the new processed words
        self.inst["words"] = processed_words[:]

    def input_text_lowercase(self, inp_lst):
        """ This method creates a list of elements containing all the space
        seperated words from the input string and then converts each of these
        words to lowercase.

        Arguments:
            inp_lst: list of all space seperated words from input string

        Returns:
            inp_lst: list containing all the space seperated words (converted
                     to lowercase) from the input string.
        """
        for i in range(len(inp_lst)):
            new_word = inp_lst[i].lower()
            inp_lst[i] = new_word
        return(inp_lst)

    def is_alnum(self, inp_lst):
        """ This method removes all the non-alphanumeric characters from each
        space seperated word of input string (here, in the form of an input
        list inp_lst).

        Arguments:
            inp_lst: list containing all the space seperated words (converted
                     to lowercase) from the input string.

        Returns:
            inp_lst: list containing all the space seperated words (converted
                     to lowercase) from the input string, with all the non-
                     alphanumeric characters deleted.
        """
        for i in range(len(inp_lst)):
            new_word = re.sub(r'[\W_+]', '', inp_lst[i])
            inp_lst[i] = new_word
        return(inp_lst)

    def remove_num(self, inp_lst):
        """ This method removes all numbers, from each space seperated word of
        input string (here, in the form of an input list inp_lst), UNLESS the
        word consists only of numbers.

        Arguments:
            inp_lst: list containing all the space seperated words (converted
                     to lowercase) from the input string, with all the non-
                     alphanumeric characters deleted.

        Returns:
            no_num_lst: list containing all the space seperated words
                        (converted to lowercase) from the input string, with
                        all the non-alphanumeric characters and digits deleted.
        """
        no_num_lst = []
        for word in inp_lst:
            if not(word.isnumeric()):
                new_word = "".join(x for x in word if not(x.isnumeric()))
            else:
                new_word = word
            no_num_lst.append(new_word)
        return(no_num_lst)

    def stop_word_process(self, no_num_lst):
        """ This method removes all stopwords (words appearing in the list
        Stop_Words) from an input list no_num_lst.

        Arguments:
            no_num_lst: list containing all the space seperated words
                        (converted to lowercase) from the input string, with
                        all the non-alphanumeric characters and digits deleted.

        Returns:
            processes_words: list containing all the space seperated words
                             (converted to lowercase) from the input string,
                             with all the non-alphanumeric characters & digits
                             from each word and stopwords deleted.
        """
        Stop_Words = [
            "i", "me", "my", "myself", "we", "our",
            "ours", "ourselves", "you", "your",
            "yours", "yourself", "yourselves", "he",
            "him", "his", "himself", "she", "her",
            "hers", "herself", "it", "its", "itself",
            "they", "them", "their", "theirs",
            "themselves", "what", "which", "who",
            "whom", "this", "that", "these", "those",
            "am", "is", "are", "was", "were", "be",
            "been", "being", "have", "has", "had",
            "having", "do", "does", "did", "doing",
            "a", "an", "the", "and", "but", "if",
            "or", "because", "as", "until", "while",
            "of", "at", "by", "for", "with",
            "about", "against", "between", "into",
            "through", "during", "before", "after",
            "above", "below", "to", "from", "up",
            "down", "in", "out", "on", "off", "over",
            "under", "again", "further", "then",
            "once", "here", "there", "when", "where",
            "why", "how", "all", "any", "both",
            "each", "few", "more", "most", "other",
            "some", "such", "no", "nor", "not",
            "only", "own", "same", "so", "than",
            "too", "very", "s", "t", "can", "will",
            "just", "don", "should", "now"
        ]
        processed_words = []
        for word in no_num_lst:
            if word not in Stop_Words:
                processed_words.append(word)
        return(processed_words)

    def get_label(self):
        return(self.inst["label"])

    def get_words(self):
        return(self.inst["words"])

    def set_class(self, theClass, tlabel="last", explain=""):
        # tlabel = tag label
        self.inst["class"] = theClass
        self.inst["experiments"][tlabel] = theClass
        self.inst["explain"] = explain
        return

    def get_class_by_tag(self, tlabel):             # tlabel = tag label
        cl = self.inst["experiments"].get(tlabel)
        if cl is None:
            return("N/A")
        else:
            return(cl)

    def get_explain(self):
        cl = self.inst.get("explain")
        if cl is None:
            return("N/A")
        else:
            return(cl)

    def get_class(self):
        return self.inst["class"]

    def process_input_line(
                self, line, run=None,
                tlabel="read", inclLabel=False
            ):
        for w in line.split():
            if w[0] == "#":
                self.inst["label"] = w
                if inclLabel:
                    self.inst["words"].append(w)
            else:
                self.inst["words"].append(w)

        if not (run is None):
            cl, e = run.classify(self, update=True, tlabel=tlabel)
        return(self)


class TrainingSet(C274):
    def __init__(self):
        super().__init__()      # Call superclass
        # self.type = str(self.__class__)
        self.inObjList = []     # Unparsed lines, from training set
        self.inObjHash = []     # Parsed lines, in dictionary/hash
        self.variable = dict()  # NEW: Configuration/environment variables
        return

    def preprocess(self, mode=''):
        # using preprocess_words(mode='') in class TrainingInstance to
        # perform preprocessing for all training instances in a
        # particular training dataset
        for instance in self.inObjHash:
            instance.preprocess_words(mode)
        return

    def return_nfolds(self, num=3):
        nfolds = []
        # creating 'num' # of copies of objects of class TrainingSet()
        # and appending them in the list nfolds
        for j in range(num):
            nfolds.append(self.copy())
        all_inst = self.get_instances()
        all_lines = self.get_lines()
        # getting (using method instance_partition) the list of
        # reordered indices of training instances arranged according
        # to basic round robbin strategy (e.g. [[0,3,6],[1,4],[2,5]])
        index_lst = self.instance_partition(num)
        # clearing the old attributes of inObjHash and inObjList from
        # the copies of TrainingSet() objects and assigning new training
        # instances and lines to every TrainingSet() object in the list
        # nfolds using index_lst which contains reordered indices of
        # training instances according to round robbin strategy
        for i in range(num):
            nfolds[i].get_instances().clear()
            nfolds[i].get_lines().clear()
            for idx in index_lst[i]:
                nfolds[i].inObjHash.append(copy.deepcopy(all_inst[idx]))
                nfolds[i].inObjList.append(copy.deepcopy(all_lines[idx]))
        return(nfolds)

    def instance_partition(self, num):
        all_inst = self.get_instances()
        nfold_inst = []
        for i in range(num):
            nfold_inst.append([])
        group = 0
        # partioning indices of training instances according the basic
        # round robbin strategy (e.g. [[0,3,6],[1,4],[2,5]])
        for j in range(len(all_inst)):
            if group < num:
                nfold_inst[group].append(j)
                group += 1
            else:
                group = 0
                nfold_inst[group].append(j)
                group += 1
        return(nfold_inst)

    def copy(self):
        # returning (after making a deepcopy) an object of class
        # TrainingSet that contains the same attributes
        # (e.g., training instances) as the original object
        # of class TrainingSet
        return(copy.deepcopy(self))

    def add_training_set(self, tset):
        # adding all the training instances of tset (class
        # TrainingSet()) to an object of class TrainingSet()
        for ti in tset.get_instances():
            self.inObjHash.append(copy.deepcopy(ti))
        self.inObjList += tset.get_lines()
        return

    def set_env_variable(self, k, v):
        self.variable[k] = v
        return

    def get_env_variable(self, k):
        if k in self.variable:
            return(self.variable[k])
        else:
            return ""

    def inspect_comment(self, line):
        if len(line) > 1 and line[1] != ' ':      # Might be variable
            v = line.split(maxsplit=1)
            self.set_env_variable(v[0][1:], v[1])
        return

    def get_instances(self):
        return(self.inObjHash)      # FIXME Should protect this more

    def get_lines(self):
        return(self.inObjList)      # FIXME Should protect this more

    def print_training_set(self):
        print("-------- Print Training Set --------")
        z = zip(self.inObjHash, self.inObjList)
        for ti, w in z:
            lb = ti.get_label()
            cl = ti.get_class_by_tag("last")     # Not used
            explain = ti.get_explain()
            print("( %s) (%s) %s" % (lb, explain, w))
            if Debug:
                print("-->", ti.get_words())
        return

    def process_input_stream(self, inFile, run=None):
        assert not (inFile is None), "Assume valid file object"
        cFlag = True
        while cFlag:
            line, cFlag = safe_input(inFile)
            if not cFlag:
                break
            assert cFlag, "Assume valid input hereafter"

            if len(line) == 0:   # Blank line.  Skip it.
                continue

            # Check for comments *and* environment variables
            if line[0] == '%':  # Comments must start with % and variables
                self.inspect_comment(line)
                continue

            # Save the training data input, by line
            self.inObjList.append(line)
            # Save the training data input, after parsing
            ti = TrainingInstance()
            ti.process_input_line(line, run=run)
            self.inObjHash.append(ti)
        return


# Very basic test of functionality
def basemain():
    global Debug
    tset = TrainingSet()
    run1 = ClassifyByTarget(TargetWords)
    if Debug:
        print(run1)     # Just to show __str__
        lr = [run1]
        print(lr)       # Just to show __repr__

    argc = len(sys.argv)
    if argc == 1:   # Use stdin, or default filename
        inFile = open_file()
        assert not (inFile is None), "Assume valid file object"
        tset.process_input_stream(inFile, run1)
        inFile.close()
    else:
        for f in sys.argv[1:]:
            # Allow override of Debug from command line
            if f == "Debug":
                Debug = True
                continue
            if f == "NoDebug":
                Debug = False
                continue

            inFile = open_file(f)
            assert not (inFile is None), "Assume valid file object"
            tset.process_input_stream(inFile, run1)
            inFile.close()

    print("--------------------------------------------")
    plabel = tset.get_env_variable("pos-label")
    print("pos-label: ", plabel)
    print("NOTE: Not using any target words from the file itself")
    print("--------------------------------------------")

    if Debug:
        tset.print_training_set()
    run1.print_config()
    run1.print_run_info()
    run1.eval_training_set(tset, plabel)

    return


if __name__ == "__main__":
    basemain()
