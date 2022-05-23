% include('header.tpl', title = "Editar tarea")

    <p>Editar tarea {{no}}:</p>
    <form action="/edit/{{no}}" method="POST">
      <input type="text" name="task" value="{{old[0]}}" size="70" maxlength="100">
      <select name="status">
      % if old[1] == 1:
        <option selected value="1">pendiente</option>
        <option value="0">finalizada</option>
      % else:
        <option value="1">pendiente</option>
        <option selected value="0">finalizada</option>
      %end
      </select>
      <br>
      <input type="submit" name="save" value="save">
      <input type="submit" name="cancel" value="Cancelar">
    </form>   

% include('footer.tpl')