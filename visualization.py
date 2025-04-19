from apartment_data_db_mysql import ApartmentDataDatabase
import matplotlib.pyplot as plt
import tkinter as tk

dates = []
prices_huf = []
one_million_huf_to_eur = []
inst = ApartmentDataDatabase()
result = inst.fetch_data_from_db()
#print (result)


def visualize_and_save(succes_label=None):
    if not result:
        return "Nincsenek adatok az adatbázisban!"
    
    print("Visualizing data...")
    for row in result:
        dates.append(row[0])
        prices_huf.append(row[1])
        one_million_huf_to_eur .append(row[3])

    fig1, ax1 = plt.subplots(figsize=(10,6))
    ax1.plot(dates, prices_huf, marker='o', linestyle='-', color='r', label='HUF')
    ax1.set_xlabel('Dátum')
    ax1.set_ylabel('Atlagos négyzetméterár (HUF)', color='r')
    ax1.tick_params('y', colors='r')

    ax2 = ax1.twinx()
    ax2.plot(dates, one_million_huf_to_eur , marker='o', linestyle='-', color='b', label='1.000.000 HUF in EUR')
    ax2.set_ylabel('EUR-HUF árfolyam)', color='b')
    ax2.tick_params('y', colors='b')

    plt.xlabel('Dátum')
    plt.title('50-60 nm lakások átlagos négyzetméterár változása Debrecenben')
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper left')

    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

 # Itt kérjük be hova mentsük
    save_path = tk.filedialog.asksaveasfilename(
        defaultextension=".jpg",
        filetypes=[("JPEG files", "*.jpg")],
        title="Save visualization as JPG"
    )
    message = ""

    if save_path:
        fig1.savefig(save_path, format='jpg')
        message = f"Sikeresen mentve: {save_path}"
    else:
        message = "Mentés megszakítva."

    plt.show()  # mindig mutassuk az ábrát a mentéstől függetlenül
    return message
