import difflib

def compare_html_files(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        html1 = f1.readlines()
        html2 = f2.readlines()

    diff = difflib.unified_diff(html1, html2, lineterm='')

    diff_html = ''.join(diff)

    with open('diff.html', 'w') as f:
        f.write(diff_html)

    print("Differences saved to diff.html")


def apply_diff(file1, file2, diff_output, title="diff.html"):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        html1 = f1.readlines()
        html2 = f2.readlines()

    diff_html = difflib.HtmlDiff().make_file(html1, html2, context=True, numlines=5)

    with open(diff_output, 'w') as f:
        f.write(diff_html)

    print("Differences saved to", diff_output)

# Example usage
compare_html_files('/Users/saschatran/Documents/FS24/work/oasis/francesc/estimation/Linear_OASIS_20231227-175343.html',
                    '/Users/saschatran/Documents/FS24/work/oasis/francesc/estimation/Linear_OASIS_20240319-120852.html')

# Example usage
apply_diff('/Users/saschatran/Documents/FS24/work/oasis/francesc/estimation/Linear_OASIS_20231227-175343.html', 
           '/Users/saschatran/Documents/FS24/work/oasis/francesc/estimation/Linear_OASIS_20240319-120852.html', 
           'diff.html', )
