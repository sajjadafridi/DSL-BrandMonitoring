from langdetect import detect_langs, DetectorFactory, detect
import operator

def language_detection(text):
    ''' constrain the non-determinastic beahvour '''
    DetectorFactory.seed = 0
    languages_list = dict()
    languages = detect_langs(text)
    if len(languages) > 0:
        for lang in languages:
            la = str(lang)
            score = la.split(":")
            languages_list[score[0]] = float(score[1])
        return max(languages_list.items(), key=operator.itemgetter(1))[0]
    else:
        return None

print(language_detection("😂😂 what"))