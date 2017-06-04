import requests


# # 3849894 /home/lpmayos/Downloads/sensembed_vectors
def main():
    generate_json_file_batches()
    # save_sensembeds_to_solr()


def save_sensembeds_to_solr():
    # curl 'http://localhost:8983/solr/sensembed_vectors/update?commit=true' --data-binary @sensembeds_small.json -H 'Content-type:application/json'

    i = 1
    num_docs = 5
    while i <= num_docs:
        # url = 'http://localhost:8983/solr/sensembed_vectors/update'
        # headers = {'content-type': 'application/json'}
        # params = {"commit": "true", 'data-binary': '@sensembed_vectors/sensembed_' + str(i) + '.json'}
        # res = requests.post(url, params=params, headers=headers)
        # print res
        # print 'uploaded doc ' + str(i) + ' of ' + str(num_docs) + ' to solr'
        # i += 1

        url = 'http://localhost:8983/solr/sensembed_vectors/update'
        headers = {"content-type": "application/json"}
        params = {"commit": "true"}
        payload = open('sensembed_vectors/sensembed_' + str(i) + '.json', "rb").read()
        # payload = open('sensembeds_small.json', "rb").read()
        r = requests.post(url, data=payload, params=params, headers=headers)
        print("got back: %s" % r.text)
        print 'uploaded doc ' + str(i) + ' of ' + str(num_docs) + ' to solr'
        i += 1


def generate_json_file_batches():

    i = 0
    batch_size = 100000
    num_doc = 1

    infile = open('/home/lpmayos/Downloads/sensembed_vectors')
    outfile = open('/home/lpmayos/code/mcv_thesis/sensembed_vectors/sensembed_' + str(num_doc) + '.json', 'w')
    import ipdb; ipdb.set_trace()
    outfile.write('[')

    for line in infile:

        if i > 0 and (i + 1) % batch_size != 0:
            outfile.write(',')

        i += 1
        if i % batch_size == 0:
            import ipdb; ipdb.set_trace()
            i = 0
            outfile.write(']')
            outfile.close()
            print 'closed doc ' + str(num_doc)
            num_doc += 1
            outfile = open('/home/lpmayos/code/mcv_thesis/sensembed_vectors/sensembed_' + str(num_doc) + '.json', 'w')
            outfile.write('[')

        sense = line.split()[0]
        vector = line.split()[1:]  # 400 float numbers in string format
        outfile.write('\n\t{')
        outfile.write('\n\t\t"sense": "' + sense.replace("\\", "") + '",')
        outfile.write('\n\t\t"sensembed": ' + str([float(a) for a in vector]))
        outfile.write('\n\t}')

    outfile.write(']')
    outfile.close()


def generate_json_file():

    with open('/home/lpmayos/code/mcv_thesis/sensembed.json', 'w') as outfile:
        outfile.write('[')

        with open('/home/lpmayos/Downloads/sensembed_vectors') as data_file:
            i = 0
            for line in data_file:
                if i > 0:
                    outfile.write(',')

                sense = line.split()[0]
                vector = line.split()[1:]  # 400 float numbers in string format
                outfile.write('\n\t{')
                outfile.write('\n\t\t"sense": "' + sense + '",')
                outfile.write('\n\t\t"sensembed": ' + str([float(a) for a in vector]))
                outfile.write('\n\t}')

                i += 1
                if i % 100 == 0:
                    print i

        outfile.write(']')
        outfile.close()


if __name__ == '__main__':
    main()
