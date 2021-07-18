import copy
import random



class Biagram:
    # store all words of pos and neg worlds
    positive_dict = {}
    negative_dict = {}

    # possibility of each word in pos and neg worlds
    positive_dict_expectancy = {}
    negative_dict_expectancy = {}

    # store all couple worlds
    binary_pos_dict = {}
    binary_neg_dict = {}

    # possibility of each couple worlds
    binary_pos_dict_expectancy = {}
    binary_neg_dict_expectancy = {}

    total_positive_words_number = 0
    total_negative_words_number = 0

    l1 = 0.001
    l2 = 0.8
    l3 = 1 - (l1 + l2)
    eps = 0.1
    print(l1, l2, l3, eps)

    def __init__(self):
        f1 = open('dict/rt-polarity.pos', "r")
        self.positive_text = f1.read()

        f2 = open('dict/rt-polarity.neg', "r")
        self.negative_text = f2.read()

    def preProcessing(self):
        items_to_delete = ['.']
        for item in items_to_delete:
            self.positive_text = self.positive_text.replace(item, '')
            self.negative_text = self.negative_text.replace(item, '')

    def preprocessing_sentence(self, sentence):
        items_to_delete = ["\n", '(', ')', '--', '"', '*', ' ,', '?', ' .']
        for item in items_to_delete:
            sentence = sentence.replace(item, '')
        return sentence

    def binary_preProcessing(self):
        items_to_delete = ["\n", '(', ')', '--', '"', '*', ' ,', '?']

        for item in items_to_delete:
            self.positive_text = self.positive_text.replace(item, '')
            self.negative_text = self.negative_text.replace(item, '')

    def creating_dictionary_unary(self):
        self.total_positive_words_number = 1
        self.total_negative_words_number = 1

        for i in self.positive_text.split(' '):
            if i in self.positive_dict.keys():
                self.positive_dict[i] = self.positive_dict[i] + 1
            else:
                self.positive_dict[i] = 1
        for i in self.negative_text.split(' '):
            if i in self.negative_dict.keys():
                self.negative_dict[i] = self.negative_dict[i] + 1
            else:
                self.negative_dict[i] = 1

    def delete_unnecessary(self, nlist):
        new_list = []
        for item in nlist:
            if item != '':
                new_list.append(item)

        return new_list

    def creating_dictionary_binary(self):
        for sentence in self.positive_text.split('.'):
            one_sentence = self.delete_unnecessary(sentence.split(' '))
            if len(one_sentence) > 0:
                for word in range(len(one_sentence) - 1):
                    binary = one_sentence[word] + "|" + one_sentence[word + 1]
                    if binary in self.binary_pos_dict.keys():
                        self.binary_pos_dict[binary] += 1
                    else:
                        self.binary_pos_dict[binary] = 1

        for sentence in self.negative_text.split('.'):
            one_sentence = self.delete_unnecessary(sentence.split(' '))
            if len(one_sentence) > 0:
                for word in range(len(one_sentence) - 1):
                    binary = one_sentence[word] + "|" + one_sentence[word + 1]
                    if binary in self.binary_neg_dict.keys():
                        self.binary_neg_dict[binary] += 1
                    else:
                        self.binary_neg_dict[binary] = 1

    def calculating_binary_sentence_expectancy(self, word1, word2, expectancy_state):
        expectancy = 0

        if expectancy_state == "positive":
            words = word1+"|"+word2
            if not (words in self.binary_pos_dict.keys()):
                if not(word2 in self.positive_dict.keys()):
                    expectancy = self.l1 * self.eps
                else:
                    expectancy = self.l2*self.positive_dict_expectancy[word2] + self.l1*self.eps
            else:
                if not(word2 in self.positive_dict_expectancy.keys()):
                    expectancy = self.l3 * self.binary_pos_dict[words] + self.l1*self.eps
                else:
                    expectancy = self.l3*self.binary_pos_dict[words] + self.l2*self.positive_dict_expectancy[word2] + self.l1*self.eps

        else:
            words = word1 + "|" + word2
            if not (words in self.binary_neg_dict.keys()):
                if not (word2 in self.negative_dict.keys()):
                    expectancy = self.l1 * self.eps
                else:
                    expectancy = self.l2 * self.negative_dict_expectancy[word2] + self.l1 * self.eps
            else:
                if not (word2 in self.negative_dict_expectancy.keys()):
                    expectancy = self.l3 * self.binary_neg_dict[words] + self.l1 * self.eps
                else:
                    expectancy = self.l3 * self.binary_neg_dict[words] + self.l2 * self.negative_dict_expectancy[word2] + self.l1 * self.eps
        return expectancy


    def updating_binary_expectancy(self):
        for k in self.binary_pos_dict.keys():
            a1, a2 = str(k).split('|')
            if not(a2 in self.positive_dict_expectancy.keys()):
                self.binary_pos_dict[k] = self.l3 * self.binary_pos_dict[k] + self.l1*self.eps
            else:
                self.binary_pos_dict[k] = self.l3*self.binary_pos_dict[k] + self.l2*self.positive_dict_expectancy[a2] + self.l1*self.eps

        for k in self.binary_neg_dict.keys():
            a1, a2 = str(k).split('|')
            if not (a2 in self.negative_dict_expectancy.keys()):
                self.binary_neg_dict[k] = self.l3 * self.binary_neg_dict[k] + self.l1 * self.eps
            else:
                self.binary_neg_dict[k] = self.l3 * self.binary_neg_dict[k] + self.l2 * self.negative_dict_expectancy[a2] + self.l1 * self.eps



    def calculating_binary_expectancy(self):
        for k in self.binary_pos_dict.keys():
            a1, a2 = str(k).split('|')
            if not(a1 in self.positive_dict.keys()):
                self.binary_pos_dict[k] = 0
            else:
                self.binary_pos_dict[k] /= self.positive_dict[a1]

        for k in self.binary_neg_dict.keys():
            a1, a2 = str(k).split('|')
            if not(a1 in self.negative_dict.keys()):
                self.binary_neg_dict[k]=0
            else:
                self.binary_neg_dict[k] /= self.negative_dict[a1]


    def deleting_extra_word(self):
        positive_key_list = []
        for i in self.positive_dict.keys():
            positive_key_list.append(i)

        for k in positive_key_list:
            if self.positive_dict[k] < 2 or self.positive_dict[k] > 1000:
                self.positive_dict.pop(k)

        negative_key_list = []
        for i in self.negative_dict.keys():
            negative_key_list.append(i)

        for k in negative_key_list:
            if self.negative_dict[k] < 2 or self.negative_dict[k] > 1000:
                self.negative_dict.pop(k)


    def deleting_extra_binary_couples(self):
        binary_pos_key_list = []
        for i in self.binary_pos_dict.keys():
            binary_pos_key_list.append(i)

        for k in binary_pos_key_list:
            if self.binary_pos_dict[k] < 2 or self.binary_pos_dict[k] > 1000:
                self.binary_pos_dict.pop(k)

        binary_neg_key_list = []
        for i in self.binary_neg_dict.keys():
            binary_neg_key_list.append(i)

        for k in binary_neg_key_list:
            if self.binary_neg_dict[k] < 2 or self.binary_neg_dict[k] > 1000:
                self.binary_neg_dict.pop(k)


    def calculating_expectancy(self):
        positive_m = 0
        for k in self.positive_dict.keys():
            positive_m += self.positive_dict[k]
        for k in self.positive_dict.keys():
            self.positive_dict_expectancy[k] = self.positive_dict[k]/positive_m

        negative_m = 0
        for k in self.negative_dict.keys():
            negative_m += self.negative_dict[k]
        for k in self.negative_dict.keys():
            self.negative_dict_expectancy[k] = self.negative_dict[k]/negative_m


    def calculating_biagram_sentence_expectancy(self, sentence):
        sentence = self.preprocessing_sentence(sentence)
        sentence = sentence.split(' ')
        final_pos_expectancy = 1
        final_neg_expectancy = 1
        # calculating positive expectancy
        for i in range(1, len(sentence)):
            words = sentence[i - 1] + "|" + sentence[i]
            if not(words in self.binary_pos_dict_expectancy.keys()):
                final_pos_expectancy *= self.calculating_binary_sentence_expectancy(sentence[i-1], sentence[i], "positive")
            else:
                final_pos_expectancy *= self.binary_pos_dict_expectancy[words]
        if not(sentence[0] in self.positive_dict_expectancy.keys()):
            final_pos_expectancy *= (1/self.total_positive_words_number)
        else:
            final_pos_expectancy *= self.positive_dict_expectancy[sentence[0]]
        # calculating negative expectancy
        for i in range(1, len(sentence)):
            words = sentence[i - 1] + "|" + sentence[i]
            if not(words in self.binary_neg_dict_expectancy.keys()):
                final_neg_expectancy *= self.calculating_binary_sentence_expectancy(sentence[i-1], sentence[i], "negative")
            else:
                final_neg_expectancy *= self.binary_neg_dict_expectancy[words]
        if not (sentence[0] in self.negative_dict_expectancy.keys()):
            final_neg_expectancy *= (1 / self.total_negative_words_number)
        else:
            final_neg_expectancy *= self.negative_dict_expectancy[sentence[0]]
        if final_neg_expectancy <= final_pos_expectancy:
            return "not filter this"
        else:
            return "filter this"

    def testing(self):
        testing_list = dict()

        f1 = open('dict/pos_test.txt', "r")
        positive_test = f1.read()

        f1 = open('dict/neg_test.txt', "r")
        negative_test = f1.read()

        positive_test = positive_test.split('.')
        negative_test = negative_test.split('.')
        pos_result_test = []
        neg_result_test = []
        for sentence in positive_test:
            if not(sentence==' ' or sentence==''):
                pos_result_test.append(sentence)

        for sentence in negative_test:
            if not (sentence==' ' or sentence==''):
                neg_result_test.append(sentence)

        positive_test = copy.deepcopy(pos_result_test)
        negative_test = copy.deepcopy(neg_result_test)

        for i in range(len(positive_test)):
            testing_list[self.preprocessing_sentence(positive_test[i])] = "not filter this"
        for i in range(len(negative_test)):
            testing_list[self.preprocessing_sentence(negative_test[i])] = "filter this"
        keys = list(testing_list.keys())
        random.shuffle(keys)
        # testing_list = [(key, testing_list[key]) for key in keys]
        for key in keys:
            testing_list[key] = testing_list[key]

        correct_number = 0
        for sentence in testing_list.keys():
            if self.calculating_biagram_sentence_expectancy(sentence) == testing_list[sentence]:
                correct_number += 1

        return correct_number / len(list(testing_list.keys()))


    def calling_methods(self):
        # prepare all binary requirements
        self.binary_preProcessing()
        self.creating_dictionary_binary()
        #self.deleting_extra_binary_couples()
        # prepare all unary requirements
        self.preProcessing()

        self.creating_dictionary_unary()
        self.deleting_extra_word()
        self.calculating_expectancy()

        self.calculating_binary_expectancy()
        print(self.testing())
        #print(self.calculating_biagram_sentence_expectancy(input()))

biagram = Biagram()
biagram.calling_methods()