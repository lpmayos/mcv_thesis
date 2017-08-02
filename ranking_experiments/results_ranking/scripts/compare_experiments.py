e1 = {'log_file': '/home/lpmayos/code/mcv_thesis/results_ranking/experiment1/e1.log', 'th1': None, 'th2': 0.785}
e4 = {'log_file': '/home/lpmayos/code/mcv_thesis/results_ranking/experiment4/e4_th1_0.09.log', 'th1': 0.09, 'th2': 0.506}
e4sym = {'log_file': '/home/lpmayos/code/mcv_thesis/results_ranking/experiment4symmetrical/e4_th1_0.11.log', 'th1': 0.11, 'th2': 0.435}
e5 = {'log_file': '/home/lpmayos/code/mcv_thesis/results_ranking/experiment5/e5.log', 'th1': None, 'th2': 0.092}

e1_video24 = {'the site was very informative': 0.826113102623,
              'the site was very informative': 0.826113102623,
              'an introduction for a how to use linux tutorial': 0.808398625272,
              'the beginning of a tech show': 0.790540008829,
              'the video is a trailer for some tv show': 0.653688988895,
              'an advertisement of software': 0.647741174351,
              'guys showcasing technology for people': 0.616160650997,
              'a  man is driving a car': 0.608754675325,
              'people are hosting show': 0.603047569322,
              'there is a man who met another man in this video and he is also travelling in a car': 0.537217846291,
              'a clip with a heavy man talking to the camera': 0.493787233912,
              'two men and standing beside each other': 0.452838294515,
              'two men stand together and talk while opening credits to a show appear intermittendly': 0.449552140535,
              'two men promote their linux class': 0.436818457621,
              'two men star in how to linux': 0.365556555503,
              'two men discuss linux options with their computers': 0.354003759958,
              'two people are talking to each other': 0.349076367716,
              'two man s are talking to each other about something': 0.333734170126,
              'two overweight men talking and one of the men drives a car': 0.278976765665,
              'two men are talking': 0.273414454904}

e4_video24 = {'people are hosting show': 0.825,
              'two people are talking to each other': 0.7,
              'the video is a trailer for some tv show': 0.68,
              'guys showcasing technology for people': 0.6625,
              'two men discuss linux options with their computers': 0.625,
              'two overweight men talking and one of the men drives a car': 0.615674603175,
              'a clip with a heavy man talking to the camera': 0.6,
              'a  man is driving a car': 0.6,
              'two men are talking': 0.6,
              'two men stand together and talk while opening credits to a show appear intermittendly': 0.585,
              'an advertisement of software': 0.575,
              'two man s are talking to each other about something': 0.575,
              'two men star in how to linux': 0.5625,
              'two men promote their linux class': 0.56,
              'two men and standing beside each other': 0.55,
              'an introduction for a how to use linux tutorial': 0.5125,
              'the site was very informative': 0.475,
              'the site was very informative': 0.475,
              'there is a man who met another man in this video and he is also travelling in a car': 0.453174603175,
              'the beginning of a tech show': 0.4}

e4sym_video24 = {'two men stand together and talk while opening credits to a show appear intermittendly': 0.606111111111,
                 'two overweight men talking and one of the men drives a car': 0.595307539683,
                 'two men discuss linux options with their computers': 0.580555555556,
                 'two people are talking to each other': 0.535416666667,
                 'two men promote their linux class': 0.535138888889,
                 'people are hosting show': 0.525138888889,
                 'a clip with a heavy man talking to the camera': 0.488055555556,
                 'two men star in how to linux': 0.486666666667,
                 'there is a man who met another man in this video and he is also travelling in a car': 0.485376984127,
                 'two men and standing beside each other': 0.484722222222,
                 'guys showcasing technology for people': 0.4725,
                 'two men are talking': 0.452638888889,
                 'the video is a trailer for some tv show': 0.446666666667,
                 'two man s are talking to each other about something': 0.430138888889,
                 'an advertisement of software': 0.378392857143,
                 'a  man is driving a car': 0.37125,
                 'an introduction for a how to use linux tutorial': 0.332569444444,
                 'the beginning of a tech show': 0.296944444444,
                 'the site was very informative': 0.193055555556,
                 'the site was very informative': 0.193055555556}

e5_video24 = {'two overweight men talking and one of the men drives a car': 0.232847275748,
              'two men stand together and talk while opening credits to a show appear intermittendly': 0.198333725522,
              'a clip with a heavy man talking to the camera': 0.189056255897,
              'two man s are talking to each other about something': 0.182091160442,
              'an introduction for a how to use linux tutorial': 0.177301736183,
              'two people are talking to each other': 0.169169885877,
              'the video is a trailer for some tv show': 0.154760005208,
              'there is a man who met another man in this video and he is also travelling in a car': 0.142197933807,
              'two men star in how to linux': 0.138795434757,
              'two men discuss linux options with their computers': 0.138156530301,
              'the beginning of a tech show': 0.127557631309,
              'two men and standing beside each other': 0.121659261233,
              'the site was very informative': 0.118711667978,
              'the site was very informative': 0.118711667978,
              'two men promote their linux class': 0.117146643849,
              'a  man is driving a car': 0.102468681686,
              'two men are talking': 0.0995895451482,
              'people are hosting show': 0.0852388082885,
              'guys showcasing technology for people': 0.0755346297617,
              'an advertisement of software': 0.0600596304385}

print 'caption' + '\t' + 'e1 dist' + '\t' + 'e1_remove' + '\t' + 'e4_simil' + '\t' + 'e4_remove' + '\t' + 'e4sym_simil' + '\t' + 'e4sym_remove' + '\t' + 'e5_sim' + '\t' + 'e5_remove'
print '-------' + '\t' + '-------' + '\t' + '---------' + '\t' + '--------' + '\t' + '---------' + '\t' + '-----------' + '\t' + '------------' + '\t' + '------' + '\t' + '---------'
for caption in e1_video24:
    e1_remove = 'XXX' if e1_video24[caption] > e1['th2'] else ' '
    e4_remove = 'XXX' if e4_video24[caption] < e4['th2'] else ' '
    e4sym_remove = 'XXX' if e4sym_video24[caption] < e4sym['th2'] else ' '
    e5_remove = 'XXX' if e5_video24[caption] < e5['th2'] else ' '
    print caption + ' & ' + str(e1_video24[caption]) + ' & ' + e1_remove + ' & ' + str(e4_video24[caption]) + ' & ' + e4_remove + ' & ' + str(e4sym_video24[caption]) + ' & ' + e4sym_remove + ' & ' + str(e5_video24[caption]) + ' & ' + e5_remove

print '\\begin{longtable}{'
print '    >{\\raggedright\\arraybackslash}p{0.50\\textwidth}'
print '    >{\\raggedright\\arraybackslash}p{0.10\\textwidth}'
print '    >{\\raggedright\\arraybackslash}p{0.10\\textwidth}'
print '    >{\\raggedright\\arraybackslash}p{0.10\\textwidth}'
print '    >{\\raggedright\\arraybackslash}p{0.10\\textwidth}'
print '    }'
print '    \\caption{Experiments comparison. TODO lpmayos}'
print '    \\label{table:experiments_comparison}\\\\'
print '    \\hline'
print '    \\textbf{Caption} & \\textbf{Exp. 1} & \\textbf{Exp. 2} & \\textbf{Exp. 3} & \\textbf{Exp. 4}\\\\'
print '    \\hline'
print '    \\endfirsthead'
print '    \\multicolumn{5}{c}%'
print '    {\\tablename\\ \\thetable\\ -- \\textit{Continued from previous page}} \\\\'
print '    \\hline'
print '    \\textbf{Caption} & \\textbf{Exp. 1} & \\textbf{Exp. 2} & \\textbf{Exp. 3} & \\textbf{Exp. 4}\\\\'
print '    \\hline\\\\'
print '    \\endhead'
print '    \\hline \\multicolumn{5}{r}{\\textit{Continued on next page}} \\\\'
print '    \\endfoot'
print '    \\hline'
print '    \\endlastfoot\\\\'

for caption in e1_video24:
    e1_txt = str(round(e1_video24[caption], 3)) if e1_video24[caption] < e1['th2'] else '\\underline{' + str(round(e1_video24[caption], 3)) + '}'
    e4_txt = str(round(e4_video24[caption], 3)) if e4_video24[caption] > e4['th2'] else '\\underline{' + str(round(e4_video24[caption], 3)) + '}'
    e4sym_txt = str(round(e4sym_video24[caption], 3)) if e4sym_video24[caption] > e4sym['th2'] else '\\underline{' + str(round(e4sym_video24[caption], 3)) + '}'
    e5_txt = str(round(e5_video24[caption], 3)) if e5_video24[caption] > e5['th2'] else '\\underline{' + str(round(e5_video24[caption], 3)) + '}'
    print caption + ' & ' + e1_txt + ' & ' + e4_txt + ' & ' + e4sym_txt + ' & ' + e5_txt + '\\\\'

print '\\end{longtable}'
