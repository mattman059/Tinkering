  <div class="form-control col white-balls item-powerball">4</div>
  <div class="form-control col white-balls item-powerball">11</div>
  <div class="form-control col white-balls item-powerball">38</div>
  <div class="form-control col white-balls item-powerball">51</div>
  <div class="form-control col white-balls item-powerball">68</div>
  <div class="form-control col powerball item-powerball">5</div>

  view-source:https://www.powerball.com/previous-results?gc=powerball&sd=2023-12-02&ed=2023-12-27

  1997-11-01
  2023-12-28

  function clickLoadMore() {
    const el = document.querySelector("#loadMore");
    el.addEventListener("click",
      e => {
        e.preventDefault();

        const gc = document.querySelector("#GameCode").value;
        const sd = document.querySelector("#StartDate").value;
        const ed = document.querySelector("#EndDate").value;
        const pg = parseInt(el.dataset["val"]);
        const max = parseInt(el.dataset["max"]);

        var args = { gc: gc };
        if (sd) {
          args.sd = sd;
        }
        if (ed) {
          args.ed = ed;
        }
        args.pg = pg;

        if (pg >= max) {
          el.classList.add("d-none");
        }
        el.dataset["val"] = pg + 1;
        updateContent(args, true);

      });
    };


    https://www.powerball.com/previous-results?gc=powerball&sd=1997-11-01&ed=2023-12-28&pg=13