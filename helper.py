import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import jieba
from sklearn.decomposition import LatentDirichletAllocation

def chinese_word_cut(mytext):
    return " ".join(jieba.cut(mytext))

def get_custom_stopwords(stop_words_file):
    with open(stop_words_file) as f:
        stopwords = f.read()
    stopwords_list = stopwords.split('\n')
    custom_stopwords_list = [i for i in stopwords_list]
    return custom_stopwords_list

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
#     print()
    
def lda_on_chinese_articles_with_param(df, n_topics, 
                            col_content, 
                            stopwords, 
                            n_features, 
                            max_df, 
                            min_df,
                            n_top_words):
    articles_cutted = df[col_content].apply(chinese_word_cut)
    vect = CountVectorizer(max_df = max_df, 
                       min_df = min_df, 
                       token_pattern=u'(?u)\\b[^\\d\\W]\\w+\\b', 
                       stop_words=frozenset(stopwords))
    tf = vect.fit_transform(articles_cutted)
    lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=50,
                                    learning_method='online',
                                    learning_offset=50.,
                                    random_state=0)
    lda.fit(tf)
    print_top_words(lda, vect.get_feature_names(), n_top_words)
    return lda, tf, vect