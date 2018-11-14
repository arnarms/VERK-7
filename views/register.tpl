% include("./views/header.tpl")

<div>

        <h1> Register  </h1>

        <form action="/register" method="post">
          <p>name:</p> <input name="name" type="text" />
          <p>username:</p> <input name="username" type="text" />
          <p>password:</p> <input name="password" type="password" /><br/>
          <input type="submit" value="Register" />
        </form>

</div>
% include("./views/footer.tpl")
