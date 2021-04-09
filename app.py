from flask import Flask,render_template,request 
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity,linear_kernel    
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def load_data(data):
    df= pd.read_csv(data, sep= ';', error_bad_lines= False, encoding= 'latin-1')
    df=df.head(500)
    return df

def search_term_if_not_found(term,df):
    term = term.capitalize()
    result_df= df[df['Book-Title'].str.contains(term)]
    return result_df['Book-Title'].iloc[0]    

def vectorize_text_to_cosine_max(data):
    count_vec= CountVectorizer()
    cv_mat= count_vec.fit_transform(data)
    cosine_sim=cosine_similarity(cv_mat)
    return cosine_sim
def get_recommendation(title,cosine_sim_mat,df,num_of_rec=8):
    course_indices=pd.Series(df.index,index=df['Book-Title']).drop_duplicates()
    idx=course_indices[title]
    sim_scores=list(enumerate(cosine_sim_mat[idx]))
    sim_scores= sorted(sim_scores,key=lambda x:x[1],reverse=True)
    selected_course_indices=[i[0] for i in sim_scores[1:]]
    selected_course_score=[i[0] for i in sim_scores[1:]]
    result_df= df.iloc[selected_course_indices]   
    result_df['similarity score']=selected_course_score
    final_recommeded= result_df[['Book-Title','Book-Author','Year-Of-Publication','similarity score','Image-URL-L']]
    return final_recommeded.head(num_of_rec)
df=load_data('https://raw.githubusercontent.com/tttgm/fellowshipai/master/book_crossing_dataset/BX-Books.csv')
cosine_sim_mat=vectorize_text_to_cosine_max(df['Book-Title'])
def get_suggestions():
    data = pd.read_csv("https://raw.githubusercontent.com/sahilpocker/Book-Recommender-System/master/Dataset/books.csv")
    return list(data['title'].str.capitalize())
@app.route('/') # default route
def new():
  df=pd.read_csv('https://raw.githubusercontent.com/Diane10/movies/main/popular_book.csv')
  titles = df['book_title']
  authors=df['book_author']
  years=df['year_of_publication']
  ratings=df['book_rating']
  images = df['image_url_l']

  df_rating=pd.read_csv('https://raw.githubusercontent.com/Diane10/movies/main/mostrated.csv')
  titles_rating = df_rating['book_title']
  authors_rating=df_rating['book_author']
  # years=df['year_of_publication']
  scores_rating=df_rating['ratings']
  images_rating = df_rating['image_url_l']
  return render_template('page-index-1.html', ratings=ratings,title = titles,author=authors,year = years,image=images,titles_rating=titles_rating,authors_rating=authors_rating,scores_rating=scores_rating,images_rating=images_rating)
@app.route('/Ratingsreviews', methods = ['POST']) # default route
def Ratingsreviews():
  user_review = request.form['user_review']
  # searchdf = df[df['Book-Title']== user_review]
  # searchtitles = searchdf['Book-Title']
  # searchauthors= searchdf['Book-Author']
  # searchyears= searchdf['Year-Of-Publication']
  return render_template('result.html',message = user_review)
@app.route('/predict', methods = ['POST']) # /result route Ratingsreviews
def predict():
  name = request.form['book_name']
  searchdf = df[df['Book-Title']== name]
  searchtitles = searchdf['Book-Title']
  searchauthors= searchdf['Book-Author']
  searchyears= searchdf['Year-Of-Publication']
  # scores=result['similarity score']
  searchimages = searchdf['Image-URL-L']
  df_rating=pd.read_csv('https://raw.githubusercontent.com/Diane10/movies/main/mostrated.csv')
  titles_rating = df_rating['book_title']
  authors_rating=df_rating['book_author']
  # years=df['year_of_publication']
  scores_rating=df_rating['ratings']
  images_rating = df_rating['image_url_l']
  if name is not None:
    try :
      result= get_recommendation(name,cosine_sim_mat,df,8)
      titles = result['Book-Title']
      authors=result['Book-Author']
      years=result['Year-Of-Publication']
      # scores=result['similarity score']
      images = result['Image-URL-L']
      suggestions= get_suggestions()
    except:
      name= search_term_if_not_found(name,df)
      searchdf = df[df['Book-Title']== name]
      searchtitles = searchdf['Book-Title']
      searchauthors= searchdf['Book-Author']
      searchyears= searchdf['Year-Of-Publication']
      # scores=result['similarity score']
      searchimages = searchdf['Image-URL-L']
      result= get_recommendation(name,cosine_sim_mat,df,8)
      titles = result['Book-Title']
      authors=result['Book-Author']
      years=result['Year-Of-Publication']
      # scores=result['similarity score']
      images = result['Image-URL-L']
      suggestions= get_suggestions()
  return render_template('Recommender.html',titles_rating=titles_rating,authors_rating=authors_rating, scores_rating=scores_rating,images_rating=images_rating,title = titles,author=authors,year = years,image=images,suggestions=suggestions,searchtitles=searchtitles,searchauthors=searchauthors,searchyears=searchyears,searchimages=searchimages)
if __name__ == '__main__':
    app.run(debug=True)
