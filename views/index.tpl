<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-+0n0xVW2eSR5OomGNYDnhzAbDsOXxcvSN1TPprVMTNDbiYZCxYbOOl7+AMvyTG2x" crossorigin="anonymous">
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.25/css/dataTables.bootstrap5.css">
    <title>Tareas</title>
  </head>
<body>

<div class="container">
<h1>TODO app</h1>
<p><a href="/register">Acceso al formulario de registro</a></p>
<p><b>Añadir una nueva tarea:</b></p>
<form action="/new" method="POST">
    <div class="form-group">
    <label for="task">Tarea</label>
    <input type="text" class="form-control" size="70" maxlength="100" name="task">
    </div>
    <button type="submit" class="btn btn-primary" name="save" value="Guardar">Guardar</button>

</form>
<p><b>Las tareas actuales son las siguientes:</b></p>
<table class="table table-striped" id="data">
    <thead>
    <tr>
        <th>ID</th>
        <th>Tarea</th>
        <th>Estado</th>
        <th>Editar</th>
        <th>Borrar</th>
        <th>Acciones</th>
    </tr>
    </thead>
    <tbody>
    %for row in rows:
    <tr>
        <td>{{row[0]}}</td>
        %if row[2] == 0:
            <td><del>{{row[1]}}</del></td>
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
    </tbody>
</table>
</div>
<script type="text/javascript" charset="utf8" src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.10.25/js/jquery.dataTables.js"></script>
<script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.10.25/js/dataTables.bootstrap5.js"></script>
<script>
    $(document).ready(function () {
      $('#data').DataTable({
        "language": {
            "url": "//cdn.datatables.net/plug-ins/1.10.19/i18n/Spanish.json"
        },
        columns: [
          null,
          null,
          null,
          {orderable: false, searchable: false},
          {orderable: false, searchable: false},
          {orderable: false, searchable: false},
          ],
      });
    });
</script>
</body>
</html>