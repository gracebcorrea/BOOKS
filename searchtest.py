if request.method == 'POST':

    result=[]
    results=[]
    checkedvalue = "author"    #request.form.get("checkedvalue")
    SQLquerry = "Agatha Christie" #request.form.get("SQLquerry")

    #SQL= ("SELECT * FROM books WHERE (:checkedvalue ) = (:SQLquerry)",{"checkedvalue" :checkedvalue , "SQLquerry" : SQLquerry})
    SQL = "SELECT id, title, author, isbm, year FROM public.books  WHERE [:checkedvalue] = [:SQLquerry]"
    Parametros = "{'checkedvalue' : checkedvalue, 'SQLquerry': SQLquerry}"

    if db.execute(SQL, Parametros).fetchall():
       i=0
       x = len(SQL)
       while i <= len(items):
          results.append([id], [title], [author], [isbm],[year])

          print(x, result)
          return render_template("SQLresults.html" , checkedvalue = checkedvalue, SQLquerry = SQLquerry ,x = x, result = [result] )
          i += 1

    else:
        return render_template("Alerts.html", tipo="alert alert-danger", message="no results for this search",  NewUrl="/search")
