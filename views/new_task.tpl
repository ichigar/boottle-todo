% include('header.tpl', title = "Nueva tarea")

    <p>Añadir una nueva tarea a la lista:</p>
    <form action="/new" method="POST">
      <input type="text" size="70" maxlength="100" name="task">
      <input type="submit" name="save" value="save">
    </form>   

% include('footer.tpl')