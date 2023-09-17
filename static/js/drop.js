// TODO drag'n'drop и отправка в конвертер видео в gif

function dropHandler(ev) {
    ev.preventDefault();
    if (ev.dataTransfer.items) {
      [...ev.dataTransfer.items].forEach((item, i) => {
        if (item.kind === "file") {
          const file = item.getAsFile();
          alert(`Добавление файла ${file.name} будет реализованно в следующей версии`);
        }
      });
    } else {
      [...ev.dataTransfer.files].forEach((file, i) => {
        alert(`… file[${i}].name = ${file.name}`);
      });
    }
  }

  function dragOverHandler(ev) {
      ev.preventDefault();
  }