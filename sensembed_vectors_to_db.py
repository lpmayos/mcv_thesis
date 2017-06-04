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

    infile_name = '/home/lpmayos/Downloads/sensembed_vectors'  # 'sensembeddings.txt'

    i = 1
    batch_size = 100000
    num_doc = 1
    total_lines = sum(1 for line in open(infile_name))

    infile = open(infile_name)
    outfile = open('sensembed_vectors/sensembed_' + str(num_doc) + '.json', 'w')
    outfile.write('[')

    for line in infile:

        sense = line.split()[0]
        vector = line.split()[1:]  # 400 float numbers in string format
        outfile.write('\n\t{')
        outfile.write('\n\t\t"sense": "' + sense.replace("\\", "") + '",')
        outfile.write('\n\t\t"sensembed": ' + str([float(a) for a in vector]))
        outfile.write('\n\t}')

        # if we are not about to close the doc, add a separator
        end_batch = i % batch_size == 0
        lines_remaining = i < total_lines
        if not end_batch and lines_remaining:
            outfile.write(',')
        else:
            outfile.write(']')
            outfile.close()
            if lines_remaining:
                num_doc += 1
                outfile = open('sensembed_vectors/sensembed_' + str(num_doc) + '.json', 'w')
                outfile.write('[')
        i += 1


if __name__ == '__main__':
    main()
