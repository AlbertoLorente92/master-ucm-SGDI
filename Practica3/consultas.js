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
  return db.sgdi.mapReduce(c1,c2,{out:"outputMR1"},{query:{}})
}


// Listado de numero de aficiones-numero de usuarios, es decir, cuAntos
// usuarios tienen 0 aficiones, cuantos una aficion, cuantos dos aficiones, etc.
function mr2(){
	return "";
}


// Listado de pais-numero de usuarios que tienen mas posts que contestaciones.
function mr3(){
	return "";
}


// Listado de pais-media de posts por usuario.
function mr4(){
	return "";
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
  return key,Array.sum(value)
};

