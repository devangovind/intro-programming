import matplotlib.pyplot as plt

def create_pie_chart(data, labels, title):
    colors =  ['#1f77b466', '#ff7f0e66', '#2ca02c66']   # Adjusted opacity
    explode = [0.05] * len(data)  # To slightly separate the slices

    fig, ax = plt.subplots(figsize=(8, 6))  # Adjusted for a better aspect ratio

    wedges, texts, autotexts = ax.pie(
        data,
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        explode=explode,
        pctdistance=0.85,
        wedgeprops=dict(width=0.3)
    )

    plt.setp(autotexts, size=8, weight="bold", color="white")  # Adjusted text size

    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig.gca().add_artist(centre_circle)

    ax.axis('equal')

    legend_labels = labels
    ax.legend(wedges, legend_labels, title="Resources", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    plt.title(title)
    plt.tight_layout()  # Removed rect adjustment
    plt.show()