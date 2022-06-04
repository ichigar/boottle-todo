% include('header.tpl', title = "TODO app")
<h1>TODO app</h1>
<p><a href="/register">Acceso al formulario de registro</a></p>
<p><b>Añadir una nueva tarea:</b></p>
<form action="/" method="POST">
    <fieldset>
        <div>    
            {{ form.task.label }}:
            {{ form.task }}
            %if form.task.errors:
            <ul class="errors">
                %for error in form.task.errors:
                    <li>{{ error }}</li>
                %end
            </ul>
            %end
        </div>
        <div>
            {{ form.save }}    
        </div>
    </fieldset>
</form>
<p><b>Las tareas actuales son las siguientes:</b></p>
<table border="1">
    <tr>
        <th>ID</th>
        <th>Tarea</th>
        <th>Estado</th>
        <th colspan="3">Acciones</th>
    </tr>
    %for row in rows:
    <tr>
        <td>{{row[0]}}</td>
        %if row[2] == 0:
            <td class="finalizado">{{row[1]}}</td>
            <td>Cerrada</td>
        %else:
            <td>{{row[1]}}</td>
            <td>Abierta</td>
        %end
            
        <td>
            <form action="/edit/{{row[0]}}" method="GET">
                <input type="submit" name="save" value="Editar">
            </form>
        </td>
        <td>
            <form action="/delete/{{row[0]}}" method="GET">
                <input type="submit" name="delete" value="Borrar">
            </form>
        </td>
        <td>
            %if row[2] == 0:
                <form action="/open/{{row[0]}}" method="POST">
                    <input type="submit" name="open" value="Abrir">
                </form>
            %else:
                <form action="/close/{{row[0]}}" method="POST">
                    <input type="submit" name="close" value="Cerrar">
                </form>
            %end
        </td>
    </tr>
    %end
</table>
% include('footer.tpl')