<script lang="ts">
    async function onSubmit(event) {
        const data = new FormData(this);

        const response = await fetch(this.action, {
            method: 'POST',
            body: JSON.stringify(Object.fromEntries(data)),
        });

    }
</script>

<form class="container" on:submit|preventDefault={onSubmit} action="http://127.0.0.1:8888/appeal">

  <div class="my-2 my-lg-0 bg-white shadow-soft border rounded border-gray-200 p-2 p-lg-3">
    <div class="text-center text-md-center mb-4 mt-md-0">
      <h1>Форма обращения</h1>
    </div>
    <div class="row">
      <div class="col-md-6">
        <label class="form-label">Имя</label>
        <input type="text" class="form-control mb-3" name="name">
      </div>
      <div class="col-md-6">
        <label class="form-label">Фамилия</label>
        <input type="text" class="form-control mb-3" name="surname">
      </div>
    </div>
    <div class="row">
      <div class="col-md-6">
        <label class="form-label">Отчество</label>
        <input type="text" class="form-control mb-3" name="patronymic">
      </div>
      <div class="col-md-6">
        <label class="form-label">Телефон</label>
        <input type="tel" class="form-control mb-3" name="phone_number">
      </div>
    </div>
    <div class="col-12">
      <label class="form-label">Обращение</label>
      <textarea rows="5" class="form-control mb-3" name="description"></textarea>
    </div>
    <div class="text-center">
      <input class="btn btn-primary mt-2" type="submit">
    </div>
  </div>
</form>

<style>
    .container {
        display: grid;
        grid-auto-flow: row;
        grid-gap: 0.5rem;
        grid-auto-rows: minmax(2rem, min-content);
    }
</style>