# The instruction:
# 1. Import the data from medical_examination.csv and assign it to the df variable.
# 2. Add an overweight column to the data. To determine if a person is overweight, first calculate their BMI by dividing their weight in kilograms by the square of their height in meters. If that value is > 25 then the person is overweight. Use the value 0 for NOT overweight and the value 1 for overweight.
# 3. Normalize data by making 0 always good and 1 always bad. If the value of cholesterol or gluc is 1, set the value to 0. If the value is more than 1, set the value to 1.
# 4. Draw the Categorical Plot in the draw_cat_plot function.
# 5. Create a DataFrame for the cat plot using pd.melt with values from cholesterol, gluc, smoke, alco, active, and overweight in the df_cat variable.
# 6. Group and reformat the data in df_cat to split it by cardio. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
# 7. Convert the data into long format and create a chart that shows the value counts of the categorical features using the following method provided by the seaborn library import: sns.catplot().
# 8. Get the figure for the output and store it in the fig variable.
# 9. Do not modify the next two lines.
# 10. Draw the Heat Map in the draw_heat_map function.
# 11. Clean the data in the df_heat variable by filtering out the following patient segments that represent incorrect data:
#       - diastolic pressure is higher than systolic (Keep the correct data with (df['ap_lo'] <= df['ap_hi']))
#       - height is less than the 2.5th percentile (Keep the correct data with (df['height'] >= df['height'].quantile(0.025)))
#       - height is more than the 97.5th percentile
#       - weight is less than the 2.5th percentile
#       - weight is more than the 97.5th percentile
# 12. Calculate the correlation matrix and store it in the corr variable.
# 13. Generate a mask for the upper triangle and store it in the mask variable.
# 14. Set up the matplotlib figure.
# 15. Plot the correlation matrix using the method provided by the seaborn library import: sns.heatmap().
# 16. Do not modify the next two lines.


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df =  pd.read_csv("medical_examination.csv")

# 2
df['overweight'] =  df.apply(
                                lambda rr: 1 if ( rr['weight']/(rr['height']/100)**2 ) > 25 else 0,
                                axis = 1

                                )

# 3
df['cholesterol'] = df.apply(

                            lambda rr: 0 if (rr['cholesterol'] == 1) else 1,
                            axis = 1

)

df['gluc'] = df.apply(

                            lambda rr: 0 if (rr['gluc'] == 1) else 1,
                            axis = 1

)


# 4
def draw_cat_plot():
    # 5
    df_cat = df.drop(columns = ["sex", "id", "age", "height", "weight", "ap_hi", "ap_lo"])
    df_cat = pd.melt( df_cat, id_vars = 'cardio')

    # 6
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='total')

    # 7
    import seaborn as sns
    import matplotlib.pyplot as plt
    
    

    # 8
    figg = sns.catplot(data= df_cat,# Datanya yang diproses di pd.melt()
            x = 'variable',  # Kolom 'variable' as the x-axis
            y = 'total',
            hue = 'value',   # value untuk setiap category di kolom variable
            col = 'cardio',  # Pisahkan berdasarkan cardio
            kind = 'bar',  # Jenis grafiknya bar chart

            )
    



    # 9
    figg.savefig('catplot.png')
    return figg.fig


# 10
def draw_heat_map():
    # 11
    # df_heat = df[(df['ap_lo'] <= df['ap_hi'])]
    df_heat = df[
                      (df['ap_lo'] <= df['ap_hi']) & 
                      (df['height'] >= df['height'].quantile(0.025)) &
                      (df['height'] <= df['height'].quantile(0.975)) &
                      (df['weight'] >= df['weight'].quantile(0.025)) &  
                      (df['weight'] <= df['weight'].quantile(0.975))

                      ]



    # df_heat = df_heat[df_heat['height'] <= df_heat['height'].quantile(0.975)]
    
    # df_heat = df_heat[df_heat['weight'] <= df_heat['weight'].quantile(0.975)]


    # 12
    # corr = df_heat.corr(numeric_only = True).round(1)
    corr = df_heat.corr(numeric_only = True)

    # 13
    maskk = np.triu(np.ones_like(corr, dtype=bool))
        

    # 14
    fig, ax = plt.subplots(figsize=(10, 8))
    # 15
    sns.heatmap(corr, mask=maskk, annot=True, fmt = ".1f", center = 0, vmax = .3, vmin=-.1, square = True, cbar_kws={"shrink": 0.5})
    plt.title("Correlation Matrix with Triangle Mask")
    plt.show()

    # 16
    fig.savefig('heatmap.png')
    return fig


    
