#!/usr/bin/env python3
import play
import sys

def my_help():
  mes = '''
  użycie: koksszachy [ARGUMENT]

  Lubisz grać w szachy? Podobał ci się chess.com lub lichess? W takim razie pokochasz KoksSzachy! <3
  Po więcej informacji odwiedź: https://github.com/a1eaiactaest/KoksSzachy

  argumenty:
  -h, --help    pokaż tą wiadomość
  -p, --play    zagraj w swoje ulubione szachy! 
  -d, --docs    przeczytaj dokumentację

  '''
  print(mes)

def main():
  try: 
    argument = sys.argv[1]
    if argument == '--play' or argument == '-p':
      play.run()

    if argument == '--docs' or argument == '-d':
      import webbrowser
      webbrowser.open_new_tab('https://github.com/a1eaiactaest/KoksSzachy/blob/main/README.md')

    if argument == '--help' or argument == '-h':
      my_help()

  except Exception:
    my_help()
    print("error: ", sys.exc_info()[0])
    raise

if __name__ == '__main__':
  main()
