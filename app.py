import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

st.markdown("""
<style>
.section-gap {
    margin-top: 60px;   /* controls vertical spacing */
}         
.stat-card {
    background-color: #0e1117;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
}
.stat-title {
    font-size: 18px;
    font-weight: 600;
    color: white;
    min-height: 48px; /* KEY FIX */
}
.stat-value {
    font-size: 36px;
    font-weight: 800;
    color: white;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):

        # Stats Area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
        st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-title">Total Messages</div>
                    <div class="stat-value">{num_messages}</div>
                </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-title">Total Words</div>
                    <div class="stat-value">{words}</div>
                </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-title">Media Shared</div>
                    <div class="stat-value">{num_media_messages}</div>
                </div>""", unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-title">Links Shared</div>
                    <div class="stat-value">{num_links}</div>
                </div>""", unsafe_allow_html=True)

        # monthly timeline
        st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
            st.title('Most Busy Users')
            x,new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        most_common_df = helper.most_common_words(selected_user,df)

        fig,ax = plt.subplots()

        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
        st.title('Most common words')
        st.pyplot(fig)

        











