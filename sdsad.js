function pares(nums,) {
  let pares = [];
  for (let i = 0; i < nums.length; i++) if (nums[i] % 2 == 0) pares.push(
    nums[i],
  );
  return pares;
}
function encontrarEnv(nums,) {
  let resultados = [];
  resultados.push(menor(nums,),);
  resultados.push(maior(nums,),);
  console.log(`maior ${resultados[1]} menor ${resultados[0]}`,);
}
function maior(n,) {
  let temp = 0;
  for (let i = 0; i < n.length; i++) if (temp < n[i]) temp = n[i];
  return temp;
}
function menor(n,) {
  let temp = n[0];
  for (let i = 0; i < n.length; i++) if (temp > n[i]) temp = n[i];
  return temp;
}
function tratarTemp(temps,) {
  let media = 0;
  let acima = 0;
  let abaixo = 0;
  for (let i = 0; i < temps.length; i++) media+=temps[i];
  media/=temps.length;
  for (let i = 0; i < temps.length; i++) {
    if(media > temps[i]){
        abaixo+=1
    }else if(media <= temps[i]){
        acima+=1
    }
  }
  console.log(`acima de ${media}: ${acima} \nabaixo de ${media}: ${abaixo} `)
}
