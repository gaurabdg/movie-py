import re, os

def time_stamp(l):
  if l[:2].isnumeric() and l[2] == ':':
    return True
  return False

def letters(line):
  if re.search('[a-zA-Z]', line):
    return True
  return False

def blank(line):
  l = line.strip()
  if not len(l):
    return True
  if l.isnumeric():
    return True
  if time_stamp(l):
    return True
  if l[0] == '(' and l[-1] == ')':
    return True
  if not letters(line):
    return True
  return False

def lowercase_letter_or_comma(letter):
  if letter.isalpha() and letter.lower() == letter:
    return True
  if letter == ',':
    return True
  return False

def parse_and_append(lines):
  new_lines = []
  for line in lines[1:]:
    if blank(line):
      continue
    elif len(new_lines) and lowercase_letter_or_comma(line[0]):
      new_lines[-1] = new_lines[-1].strip() + ' ' + line
    else:
      new_lines.append(line)
  return new_lines

def convert(file_name):
  file_encoding = 'latin-1'
  lines = ""
  print(file_name)
  with open(os.path.join('../scraper/data/', file_name), encoding=file_encoding) as f:
      lines = f.readlines()
  new_lines = parse_and_append(lines)
  new_file_name = file_name[:-4] + '.txt'
  with open(os.path.join('data_txt/', new_file_name), 'w') as f:
    for line in new_lines:
      f.write(line)

def main():
  for file in os.listdir("../scraper/data/"):
    convert(file)

if __name__ == '__main__':
    main()

