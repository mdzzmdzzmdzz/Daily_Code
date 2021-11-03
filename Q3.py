import jieba
from pyhanlp import *
import thulac


def get_label():
    print('################get label################')
    train = open('pku_training.utf8', mode='r')
    label = []
    for line in train:
        label = label + line.strip('\n').split('  ')
    train.close()
    return label


def cut_words(cut_method='jieba'):
    print('################cut words################')
    train = open('pku_training.utf8', mode='r')
    seg_list = []
    if cut_method == 'jieba':
        for line in train:
            line = line.strip('\n').replace(' ', '')
            seg_list = seg_list + list(jieba.cut(line))
    elif cut_method == 'thulac':
        thu = thulac.thulac(seg_only=True)
        for line in train:
            line = line.strip('\n').replace(' ', '')
            seg_list = seg_list + list(thu.cut(line, text=True).split())
    elif cut_method == 'hanlp':
        HanLP.Config.ShowTermNature = False
        for line in train:
            line = line.strip('\n').replace('  ','')
            for word in HanLP.segment(line):
                seg_list.append(str(word))
    train.close()
    return seg_list


def position_transform(data):
    print('################position transform################')
    i = 0
    position = []
    for word in data:
        position.append(str(i)+'-'+str(i+len(word)-1))
        i += len(word)
    return position


def evaluate(label, result, method):
    print('################evaluate################')
    label_position = position_transform(label)
    result_position = position_transform(result)
    print('################start intersection################')
    intersection = list(set(label_position).intersection(set(result_position)))
    print('################end intersection################')
    p = float(len(intersection)/len(result_position))
    r = float(len(intersection)/len(label_position))
    f1 = 2*p*r/(p+r)
    print('{}: precision {:.4} recall {:.4} f1 {:.4}'.format(method, p, r, f1))


if __name__ == '__main__':
    label = get_label()
    methods = ['jieba', 'hanlp', 'thulac']
    for method in methods:
        print('################{} method################'.format(method))
        result = cut_words(method)
        evaluate(label, result, method)



