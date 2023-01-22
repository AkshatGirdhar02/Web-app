import streamlit as st
import pandas as pd
from io import StringIO
import sys
import math
import os

# header=st.beta_container()
# uploaded_file = st.file_uploader("Choose a file")
# if uploaded_file is not None:
#     # To read file as bytes:
#     bytes_data = uploaded_file.getvalue()
#     st.write(bytes_data)

#     # To convert to a string based IO:
#     stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
#     st.write(stringio)

#     # To read file as string:
#     string_data = stringio.read()
#     st.write(string_data)

#     # Can be used wherever a "file-like" object is accepted:
#     dataframe = pd.read_csv(uploaded_file)
#     st.write(dataframe)


# if "visibility" not in st.session_state:
#     st.session_state.visibility = "visible"
#     st.session_state.disabled = False

# col1, col2,col3 = st.columns(3)

# with col1:
#     uploaded_file = st.file_uploader("Choose a file")
#     if uploaded_file is not None:
#     # To read file as bytes:
#         bytes_data = uploaded_file.getvalue()
#         st.write(bytes_data)

#     # To convert to a string based IO:
#         stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
#         st.write(stringio)

#     # To read file as string:
#         string_data = stringio.read()
#         st.write(string_data)

#     # Can be used wherever a "file-like" object is accepted:
#         dataframe = pd.read_csv(uploaded_file)
#         st.write(dataframe)

# with col2:
#     weights = st.text_input(
#         "Enter the weights 👇",
#     )

#     if weights:
#         st.write("You entered: ", weights)


# with col2:
#     impacts= st.text_input(
#         "Enter the impacts 👇",
#     )

#     if impacts:
#         st.write("You entered: ", impacts)

# with col3:
#     email_receiver=st.text_input("Enter your email 👇 ")
#     if email_receiver:
#         st.write("You entered: ",email_receiver)
#     # if st.button("Send Email"):

def euclidian_dist(row, ideal_best,ncol):
    dist = 0
    for i in range(ncol):
        dist = dist+(row[i]-ideal_best[i])**2
    return math.sqrt(dist)

def main():
    # If number of arguments are not correct
    uploaded_file = st.file_uploader("Choose a file")
    weights = st.text_input(
        "Enter the weights 👇",
    )
    impacts= st.text_input(
        "Enter the impacts 👇",
    )
    data = pd.read_csv(uploaded_file)
    nrow = data.shape[0]
    final = data.iloc[:, 1:]
    ncol = final.shape[1]
    for i in final.columns:#col
        sum = 0
        for j in range(nrow): 
            sum = sum+final.loc[j, i]**2
        final[i] = round(final[i]/math.sqrt(sum), 4)
    w1 = weights
    w = []
    for i in w1.split(','):
        w.append(int(i))
    j = 0
    for i in final.columns:
        final[i] = round(final[i]*w[j], 4)
        j += 1
    impact_st = impacts
    impact = []
    for i in impact_st.split(','):
        impact.append(i)
            #check for number of weights and number of impacts
    if(len(w)!=len(impact)):
        print("Number of weights and impacts are not same")
        exit(1)
    ideal_best = []
    ideal_worst = []
    dist_ideal_best=[]
    dist_ideal_worst=[]
    j = 0
    for i in final.columns:
        if (impact[j] == "+"):
            ideal_best.append(final[i].max())
            ideal_worst.append(final[i].min())
        else:
            ideal_best.append(final[i].min())
            ideal_worst.append(final[i].max())
        j+=1
    j = 0
    for i in range(final.shape[0]):
        dist_from_ideal_best = euclidian_dist(final.iloc[i,:], ideal_best,ncol)
        dist_from_ideal_worst = euclidian_dist(final.iloc[i,:], ideal_worst,ncol)
        dist_ideal_best.append(dist_from_ideal_best)
        dist_ideal_worst.append(dist_from_ideal_worst)
    final['S+'] = dist_ideal_best
    final['S-'] = dist_ideal_worst
    performance_score = []
    for i in range(nrow):
        p_score = (dist_ideal_worst[i])/(dist_ideal_best[i]+dist_ideal_worst[i])
        performance_score.append(round(p_score, 4))
    data['Topsis score'] = performance_score
    data['Rank'] = (data['Topsis score'].rank(method='max', ascending=False))
    data = data.astype({'Rank': int})
    st.write(data)
            #Now we will write data to csv file.
            # data.to_csv(sys.argv[4], index=False)
    # print(data)

if __name__=="__main__":
    main()

