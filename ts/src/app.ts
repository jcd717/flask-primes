/*
Le compilateur closure JS de Google renomme certaines propriétés du retour de l'API
Donc je ne l'utilise pas ici
Génération du JS:
tsc -p ./tsconfig.dev.json
avec --watch en cours de dev

D'après Google
Solution: Be Consistent in Your Property Names
This solution is pretty simple. For any given type or object, use dot-syntax or quoted strings exclusively. 
Don't mix the syntaxes, especially in reference to the same property.
Also, when possible, prefer to use dot-syntax, as it supports better checks and optimizations. 
Use quoted string property access only when you don't want Closure Compiler to do renaming, 
such as when the name comes from an outside source, like decoded JSON. 

*/

namespace Global {
  export let apiNext=(document.getElementById('apiNext') as HTMLInputElement).value;
  // export let apiAllAndNext=(document.getElementById('apiAllAndNext') as HTMLInputElement).value;

  export let valeurCompteur=document.getElementById('valeurCompteur') as HTMLSpanElement;
  export let containerPrimes=document.getElementById('containerPrimes') as HTMLDivElement;
  export let isPrime=document.getElementById('isPrime') as HTMLSpanElement;
  export let hostname=document.getElementById('hostname') as HTMLDivElement;
  export let IP=document.getElementById('IP') as HTMLDivElement;
  export let primesLength=document.getElementById('primesLength') as HTMLElement;
  export let listPrimes=document.getElementById('listPrimes') as HTMLDivElement;
  export let stringNombre=(document.getElementById('stringNombre') as HTMLInputElement).value;
  export let stringPremier=(document.getElementById('stringPremier') as HTMLInputElement).value;
  export let stringTrouvé=(document.getElementById('stringTrouvé') as HTMLInputElement).value;
  export let stringElementNombre=document.getElementById('stringElementNombre') as HTMLElement;
  export let stringElementPremier=document.getElementById('stringElementPremier') as HTMLElement;
  export let stringElementTrouvé=document.getElementById('stringElementTrouvé') as HTMLElement;
  export let buttonPlus=document.getElementById('button-plus') as HTMLButtonElement;
}

Global.buttonPlus.addEventListener('click', addCompteur);

// appel d'une API JSON
async function myFetch(url:string) {
  try {
    let res = await fetch(url);
    return await res.json();
  } 
  catch (error) {
    console.log(error);
  }
}

// Appel de l'API next
async function addCompteur() {
  let next=await myFetch(Global.apiNext); // appel de l'API
  remplir(next);
  return next;
}

function remplir(datas:any,listeEntiere:boolean=false):void {
  Global.valeurCompteur.textContent=datas['counter'];
  if(datas['counter']===1) { // la session a dû être réinitialiser
    listeEntiere=true;
    datas['listPrimes']=[];
    Global.containerPrimes.style.display='none';
  }
  else {
    Global.containerPrimes.style.display='grid'; // doit être ce qui est défini dans .container
  }
  Global.isPrime.hidden=!datas['isPrime'];
  Global.hostname.textContent=datas['hostname'];
  Global.IP.textContent=datas['IP'];
  let primesLengthValue= (Global.primesLength.textContent===null)?0: parseInt(Global.primesLength.textContent,10); // null ne doit, normalement, jamais arriver
  if(listeEntiere) {
    Global.primesLength.textContent=(datas['listPrimes'].length).toString();
    Global.listPrimes.textContent='';
    datas['listPrimes'].forEach(function(val:number,i:number,tab:Array<number>) {
      Global.listPrimes.textContent+=val.toString();
      if(i!=tab.length-1) {
        Global.listPrimes.textContent+=','
      }
    });
  }
  else if(datas['isPrime']) {
    primesLengthValue++;
    Global.primesLength.textContent=primesLengthValue.toString();
    Global.listPrimes.textContent+=((primesLengthValue<=1)?'':', ')+datas['counter'].toString();
  }
  let s=(primesLengthValue<2)? '' : 's';
  Global.stringElementNombre.textContent=Global.stringNombre+s;
  Global.stringElementPremier.textContent=Global.stringPremier+s;
  Global.stringElementTrouvé.textContent=Global.stringTrouvé+s;
}


// l'interrupteur
let cbOFF = document.getElementById('OFF') as HTMLInputElement;
cbOFF.addEventListener('change', event => {
  let off = (event.target as HTMLInputElement).checked;
  changeStateButton(!off);
});

let isLoop=false;

function changeStateButton(on: boolean) {
  Global.buttonPlus.disabled = on;

  if (on) {
    isLoop=true;
    (function loop() {
      setTimeout(async function () {
        await addCompteur();
        if(isLoop) loop();
      });
    })();

  }
  else {
    isLoop=false;
  }
}
