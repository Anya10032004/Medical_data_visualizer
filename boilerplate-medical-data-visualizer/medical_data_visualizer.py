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


    
