from django.shortcuts import render
import py.scripts.Mangakakalot as Mangakakalot

# Create your views here.
def home(request):
    
    series_instance = Mangakakalot.Series()
    series_instance.get_data_latest(1, 5) # Get Latest Data, By Default Pages 1 - 5 #

    # Access the data variables
    titles = series_instance.TITLES
    covers = series_instance.COVERS
    urls = series_instance.URLS

    # Pass the data to the template
    context = {
        'series_data' : zip(titles,covers,urls)
    }
    
    return render( request, 'main.html' , context)

def open_title(request):
    url = request.GET.get('url')
    title = request.GET.get('title')
    cover = request.GET.get('cover')
    
    series_info = Mangakakalot.SeriesInfo()
    series_info.meta(url)
    labels = series_info.LABEL
    values = series_info.VALUE
    chapters_dict = series_info.CHAPTER

    context = {
        'title': title,
        'cover': cover,
        'labels': labels,
        'values': values,
        'chapters_dict': chapters_dict,
    }

    return render(request, "title.html", context)