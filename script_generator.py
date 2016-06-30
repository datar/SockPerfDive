import os
import os.path
import sys
import generate_latency_map


def latency2map(source, dest):
    if os.path.isdir(source):
        filenames = os.listdir(source)
    else:
        filenames = [source]
    source2dest = []
    for filename in filenames:
        (basename, extname) = os.path.splitext(filename)
        if extname.upper() != '.CSV':
            continue
        source_name = os.path.join(source, filename)
        dest_in_name = os.path.join(dest, basename + '_InLatMap' + extname)
        dest_net_name = os.path.join(dest, basename + '_NetLatMap' + extname)
        source2dest.append(' '.join(['python generate_latency_map.py', source_name, dest_in_name, dest_net_name, os.linesep]))
    with open('latency2map.sh', 'w') as outfile:
        outfile.writelines(source2dest)
    outfile.close()
    return 0


def main():
    latency2map(sys.argv[1], sys.argv[2])
    return 0


if __name__ == '__main__':
    main()
