import re, os
import pandas

class srt_parser:
  def __init__(self, fname):
    self.file_name = fname

  def time_stamp(self,l):
    if l[:2].isnumeric() and l[2] == ':':
      return True
    return False

  def letters(self, line):
    if re.search('[a-zA-Z]', line):
      return True
    return False

  def blank(self, line):
    l = line.strip()
    if not len(l):
      return True
    if l.isnumeric():
      return True
    if self.time_stamp(l):
      return True
    if l[0] == '(' and l[-1] == ')':
      return True
    if not self.letters(line):
      return True
    return False

  def lowercase_letter_or_comma(self, letter):
    if letter.isalpha() and letter.lower() == letter:
      return True
    if letter == ',':
      return True
    return False

  def parse_and_append(self, lines):
    new_lines = []
    for line in lines[1:]:
      if self.blank(line):
        continue
      elif len(new_lines) and self.lowercase_letter_or_comma(line[0]):
        new_lines[-1] = new_lines[-1].strip() + ' ' + line
      else:
        new_lines.append(line)

      final_lines = []
      for nline in new_lines:
          if nline.startswith('- '):
              nline = nline[2:]
              final_lines.append(nline)
          else:
              final_lines.append(nline)

      # for line in final_lines:
      #     print(line)

    return final_lines

  def convert(self):
    file_encoding = 'latin-1'
    print(self.file_name)
    with open(os.path.join('../scraper/data/', self.file_name), encoding=file_encoding) as f:
        lines = f.readlines()
    # with open(file_name,encoding=file_encoding) as f:
    #     lines = f.readlines()
    new_lines = self.parse_and_append(lines)
    new_file_name = self.file_name[:-4] + '.txt'
    with open(os.path.join('data_txt/', new_file_name), 'w') as f:
      for line in new_lines:
        f.write(line)
    # with open(new_file_name,'w') as f:
    #     for line in new_lines:
    #         f.write(line)


def main():
  for file in os.listdir("../scraper/data/"):
    srt_parser(file).convert()
  # convert("American Psycho.srt")

if __name__ == '__main__':
    main()

