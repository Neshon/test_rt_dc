<script lang="ts">
  async function onSubmit() {
    const formData = new FormData(this)
    const data = Object.fromEntries(formData)
    try {
        await fetch(this.action, {
          method: 'POST',
          body: JSON.stringify(data),
        })
        this.reset()
    } catch(e) {
      console.log(e)
    }
  }
</script>


<form class="container" on:submit|preventDefault={onSubmit} action="http://127.0.0.1:8888/appeal">
    <div class="my-2 my-lg-0 bg-white shadow-soft border rounded border-gray-200 p-2 p-lg-3">
        <div class="text-center text-md-center mb-4 mt-md-0">
            <h1>Форма обращения</h1>
        </div>
        <div class="row">
            <div class="col-md-6">
                <label class="form-label mt-3">Имя</label>
                <input type="text" class="form-control" id="name" name="name" required>
            </div>
            <div class="col-md-6">
                <label class="form-label mt-3">Фамилия</label>
                <input type="text" class="form-control" id="surname" name="surname" required>
            </div>
        </div>
        <div class="row">
            <div class="col-md-6">
                <label class="form-label mt-3">Отчество</label>
                <input type="text" class="form-control" id="patronymic" name="patronymic" required>
            </div>
            <div class="col-md-6">
                <label for="phone_number" class="form-label mt-3">Телефон</label>
                <input type="tel" class="form-control" id="phone_number" placeholder="e.g. 9998887766" name="phone_number" required minlength="10" maxlength="15" pattern="[0-9]+">
            </div>
        </div>
        <div class="col-12">
            <label class="form-label mt-3">Обращение</label>
            <textarea class="form-control" id="description" name="description" required></textarea>
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