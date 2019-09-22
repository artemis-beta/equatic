import equatic
import argparse
import datetime

def run_calc():
    prompt = 'EquatIC[{}]: '

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-v', '--verbose', help='set logging output to DEBUG', action='store_true', default=False)
    arg_parser.add_argument('-i', '--info', help='set logging output to INFO', action='store_true', default=False)
    arg_parser.add_argument('-s', '--save', help='save output', action='store_true', default=False)
    arg_parser.add_argument('-o', '--saveas', help='save output and give name')
    args = arg_parser.parse_args()
    if args.verbose:
        log = 'DEBUG'
    elif args.info:
        log = 'INFO'
    else:
        log = 'ERROR'

    if args.save:
        if args.saveas:
            outname = args.saveas
        else:
            d = datetime.datetime.now()
            d = d.strftime('%y%m%d%H%M')
            outname = 'equatic_session_{}.log'.format(d)
        f = open(outname, 'w')

    i = 0
    out = '0'
    while True:
         inp = input(prompt.format(i))
         inp = inp.replace('_', str(out))
         if inp in ['q', 'quit', 'Q']:
             return
         out = equatic.parse(inp, debug=log)
         print(out)
         if args.save:
             f.write(str(out))
         i+=1

if __name__ == '__main__':
    run_calc()
