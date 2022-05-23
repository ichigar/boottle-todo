% include('header.tpl', title = "Editar tarea")

    <p>Editar tarea {{no}}:</p>
    <form action="/edit/{{no}}" method="POST">
      <input type="text" name="task" value="{{old[0]}}" size="100" maxlength="100">
      <select name="status">
        
        <option value="1">pendiente</option>
        <option value="0">finalizada</option>
      </select>
      <br>
      <input type="submit" name="save" value="save">
    </form>   

% include('footer.tpl')