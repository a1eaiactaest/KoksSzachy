import koksszachy
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
      koksszachy.play()

    if argument == '--docs' or argument == '-d':
      import webbrowser
      webbrowser.open_new_tab('https://github.com/a1eaiactaest/KoksSzachy/blob/main/README.md')

    if argument == '--help' or argument == '-h':
      my_help()

  except IndexError:
    my_help()
    return 0

if __name__ == '__main__':
  main()
