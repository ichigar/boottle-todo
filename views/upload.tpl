% include('header.tpl', title = "subir archivo")
<h1>Subir archivo</h1>
<form method="POST" action="/upload" enctype="multipart/form-data">
    <div>
        {{ form.file.label }}:
        {{ form.file }}
        %if form.file.errors:
        <ul class="errors">
            %for error in form.file.errors:
                <li>{{ error }}</li>
            % end
        </ul>
        %end
    </div>
    <div>
        {{ form.submit }}
    </div>
  </form>
% include('footer.tpl')