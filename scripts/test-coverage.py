# A test coverage aggregation script for html pages generated by pants
import sys

class Coverage:
  def __init__(self, num_class, line_t, line_a, branch_t, branch_a):
    self.num_class = num_class
    self.line_t = line_t
    self.line_a = line_a
    self.branch_t = branch_t
    self.branch_a = branch_a

  def add(self, num_class, line_t, line_a, branch_t, branch_a):
    self.num_class = self.num_class + num_class
    self.line_t = self.line_t + line_t
    # print "(line added %d + %d = %d)" % (self.line_a, line_a, self.line_a + line_a)
    self.line_a = self.line_a + line_a
    self.branch_t = self.branch_t + branch_t
    self.branch_a = self.branch_t + branch_a

  def report(self):
    return "C: %4d, L %6d / %6d  (%6.2f %%), B %6d / %6d  (%6.2f %%)" % (
      self.num_class,
      self.line_t, self.line_a, float(self.line_t) / self.line_a * 100.0 if self.line_a > 0 else 0.0,
      self.branch_t, self.branch_a, float(self.branch_t) / self.branch_a * 100.0 if self.branch_a > 0 else 0.0)


# get a all parent package
def get_all_parents(pkg):
  if len(pkg.split(".")) <= 3:
    return [pkg]
  list = []
  component = pkg.split(".")
  for i in range(3, len(component) + 1):
    list = list + [".".join(component[0:i])]
  return list

def get_number(item):
  try:
    return int(item)
  except ValueError:
    return 0

interested = ["com.twitter.search", "com.twitter.expertsearch", "com.twitter.typeahead"]
  
if __name__ == "__main__":
  filename = sys.argv[1]
  
  with open(filename) as f:
    lines = f.readlines()
    i= 0
    
  # find the starting line
  found = False
  while i < len(lines):
    if lines[i].startswith("Package"):
      found = True
      break
    i = i + 1
    
  if not found:
    print "Cannot find start of the report"
    exit

  # report is a map from package name to its report
  report = {}
  i = i + 1
  while i + 6 < len(lines):
    try:
      package = lines[i].strip().split()[0]
    except:
      package = ""
    if not package:
      break
    good = False
    for intr in interested:
      if package.startswith(intr):
        good = True
        break
    if not good:
      i = i + 6
      continue
          
    # print ":: %s" % (lines[i:i+5])
    
    classes =       get_number(lines[i].strip().split()[1])
    lines_tested =  get_number(lines[i + 2].strip().split("/")[0])
    lines_all =     get_number(lines[i + 2].strip().split("/")[1])
    branch_tested = get_number(lines[i + 4].strip().split("/")[0])
    branch_all =    get_number(lines[i + 4].strip().split("/")[1])
    i = i + 6

    for pkg in get_all_parents(package):
      if not pkg in report:
        # print "-- updating for %s (+%d)" % (pkg, lines_all)
        report[pkg] = Coverage(classes, lines_tested, lines_all, branch_tested, branch_all)
      else:
        # print "-- adding for %s (+%d)" % (pkg, lines_all)
        cov = report[pkg]
        cov.add(classes, lines_tested, lines_all, branch_tested, branch_all)

  keys = list(report.keys())
  keys.sort()
  spaces = " " * 40
  for pkg in keys:
    pkg_disp = pkg.replace("com.twitter", "c.t")
    print("%-60s %s" % (pkg_disp, report[pkg].report()))

            
