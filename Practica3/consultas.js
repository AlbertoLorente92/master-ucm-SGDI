/*******************************************************************************
**************************** AGGREGATION FRAMEWORK *****************************
*******************************************************************************/

// Listado de pais-numero de usuarios ordenado de mayor a menor por numero de 
// usuarios.
function agg1(){
  return db.sgdi.aggregate([{$group:{_id:"$country","num_users":{$sum:1}}},{$sort:{"num_users":-1}}])
}


// Listado de pais-numero total de posts de los 3 paises con mayor numero total 
// de posts, ordenado de mayor a menor por numero de posts.
function agg2(){
  return db.sgdi.aggregate([{$group:{_id:"$country","num_posts":{$sum:"$num_posts"}}},{$sort:{"num_posts":-1}},{$limit:3}])
}

  
// Listado de aficion-numero de usuarios ordenado de mayor a menor numero de 
// usuarios.
function agg3(){
  return db.sgdi.aggregate([{$unwind:"$likes"},{$group:{_id:"$likes","num_users":{$sum:1}}},{$sort:{"num_users":-1}}])
}  
  
  
// Listado de aficion-numero de usuarios restringido a usuarios espanoles y
// ordenado de mayor a menor numero de usuarios.
function agg4(){
  return db.sgdi.aggregate([{$unwind:"$likes"},{$match:{country:"Spain"}},{$group:{_id:"$likes","num_users":{$sum:1}}},{$sort:{"num_users":-1}}]);
}



/*******************************************************************************
********************************** MAPREDUCE ***********************************
*******************************************************************************/
  
// Listado de aficion-numero de usuarios restringido a usuarios espanoles.
function mr1(){
  return db.sgdi.mapReduce(c1,c2,{out:"outputMR1"});
}


// Listado de numero de aficiones-numero de usuarios, es decir, cuAntos
// usuarios tienen 0 aficiones, cuantos una aficion, cuantos dos aficiones, etc.
function mr2(){
	return db.sgdi.mapReduce(c3,c2,{out:"outputMR2"});
}


// Listado de pais-numero de usuarios que tienen mas posts que contestaciones.
function mr3(){
	return db.sgdi.mapReduce(c4,c2,{out:"outputMR3"});
}


// Listado de pais-media de posts por usuario.
function mr4(){
	return db.sgdi.mapReduce(c5,c6,{out:"outputMR4",finalize:c7});
}

var c1 = function f1(){
  if(this.country=="Spain" && typeof this.likes != "undefined"){
    for (var idx = 0; idx < this.likes.length; idx++) {
         var key = this.likes[idx];
         emit(key, 1);
     }
  }
};

var c2 = function f2(key,value){
  return key,Array.sum(value);
};

var c3 = function f3(){
  if(typeof this.likes == "undefined" || this.likes.length==0){
    emit(0,1);
  }else{
    emit(this.likes.length,1);
  }
};

var c4 = function f4(){
  if(this.num_posts>this.num_answers) 
    emit(this.country,1);
}

var c5 = function f5(){
  var value = {count: 1, value: this.num_posts};
  emit(this.country,value);
};

var c6 = function f6(key,value){
  reducedVal = {count: 0, value: 0 };
  for (var idx = 0; idx < value.length; idx++) {
    reducedVal.value += value[idx].value;
    reducedVal.count += value[idx].count;
  }
  return key,reducedVal;
};

var c7 = function f7(key, reducedVal){
 avg = reducedVal.value/reducedVal.count;
 return key,avg;
};
