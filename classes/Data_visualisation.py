import matplotlib.pyplot as plt

def create_pie_chart(data, labels, title):
    colors = ['#1f77b466', '#ff7f0e66', '#2ca02c66']  # Blue, Orange, Green
    explode = [0.05] * len(data)  # To slightly separate the slices

    # fig, ax = plt.subplots(figsize=(10, 8))
    fig, ax = plt.subplots(figsize=(8, 4))

    wedges, texts, autotexts = ax.pie(
        data,
        autopct='%1.1f%%',  # Show one decimal place
        startangle=90,
        colors=colors,
        explode=explode,  # Separate slices
        pctdistance=0.85,  # Percentage placement
        wedgeprops=dict(width=0.3)  # Donut width
    )

    plt.setp(autotexts, size=10, weight="bold", color="white")  # Set the properties for the autopct

    # Draw a circle at the center to make it a donut chart
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig.gca().add_artist(centre_circle)

    # Equal aspect ratio ensures that pie chart is drawn as a circle
    ax.axis('equal')

    # Add a legend
    legend_labels = labels
    ax.legend(wedges, legend_labels, title="Resources", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), frameon=False)

    plt.title(title)
    plt.tight_layout(rect=[0, 0.03, 0.75, 0.95])  # Adjust as needed
    plt.show()