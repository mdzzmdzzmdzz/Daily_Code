

def get_data(data_input):
    data_list = []
    for line in data_input:
        data_list.append(line.strip('\n'))
    dict_len = int(len(data_list)*0.7)
    max_len = len(data_list)
    word_dict = {}
    print('################get dict################')
    for i in range(0, dict_len):
        cut_list = data_list[i].strip().split('  ')
        # print(cut_list)
        for word in cut_list:
            if len(word) == 0: continue
            if len(word) > 0 and word[0] in word_dict:
                tmp_list = word_dict[word[0]]
                if word not in tmp_list:
                    tmp_list.append(word)
                    word_dict[word[0]] = tmp_list
            else:
                word_dict[word[0]] = [word]
    train_data = []
    label = []
    print('################get data and label################')
    for i in range(dict_len, max_len):
        if len(data_list[i]) == 0: continue
        train_data.append(data_list[i].replace(' ', ''))
        # print(train_data)
        label = label + data_list[i].split('  ')
    return word_dict, train_data, label


def cut_words(word_dict, train_data):
    print('################cut word################')
    result = []
    for sentence in train_data:
        maxLen = len(sentence)
        start = 0
        while start < maxLen:
            cur_cut = sentence[start]
            cur_len = 1
            if cur_cut in word_dict:
                word_list = word_dict[cur_cut]
                for key in word_list:
                    key_len = len(key)
                    if sentence[start: start+key_len] == key and key_len > cur_len:
                        cur_len = key_len
            result.append(sentence[start: start+cur_len])
            start += cur_len
    return result


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
    p = float(len(intersection)/len(label_position))
    r = float(len(intersection)/len(result_position))
    f1 = 2*p*r/(p+r)
    print('{}: precision {:.4} recall {:.4} f1 {:.4}'.format(method, p, r, f1))


if __name__ == '__main__':
    data = open('pku_training.utf8', mode='r')
    word_dict, train_data, label = get_data(data)
    cut_result = cut_words(word_dict, train_data)
    evaluate(label, cut_result, 'test')
