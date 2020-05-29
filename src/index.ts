import "reflect-metadata";
import {createConnection, getConnection, QueryBuilder, Connection, createConnections} from "typeorm";
import {Message} from "./entity/Message";
import {Book} from "./entity/Book";
import * as thecamp from 'the-camp-lib';
import * as rssParser from 'rss-parser';
import { title } from "process";

// 날짜 가져오기
const d = new Date();
const year = d.getFullYear();
const lateinitmonth = d.getMonth() + 1;
var month = "";
if(lateinitmonth + 1 < 10) { month = "0" + lateinitmonth; }  
else { month = "" + lateinitmonth; }
const day = d.getDate();
const nowdate = year + "/" + month + "/" + day
const nowdatestr = String(nowdate)

// 텔레그램 봇
async function getTelegramMessage() {
  let finalmessage: string = ""
  let getMessage = await createConnection(
    {
      "synchronize": false,
      "logging": false,
      "name" : "Message" ,
      "database": "Message.db",
      "type": "sqlite",
      "entities": [
         "src/entity/Message.ts"
      ],
      "migrations": [
         "src/migration/**/*.ts"
      ],
      "subscribers": [
         "src/subscriber/**/*.ts"
      ],
      "cli": {
         "entitiesDir": "src/entity",
         "migrationsDir": "src/migration",
         "subscribersDir": "src/subscriber"
      }
   }
  )
  .then(async conn => {
      const house = await getConnection("Message")
          .createQueryBuilder()
          .select("MESSAGE")
          .from(Message, "MESSAGE")
          .where("MESSAGE.DATE = :DATE", { DATE: nowdatestr })
          .getMany()
      if(house.length == 0){ finalmessage = "오늘은 받은 메세지가 없습니다" }
      else{
          for(var i = 0; i <= house.length - 1; i++ ){
              finalmessage += house[i].NAME + "  " + house[i].DATE + "  " + house[i].TIME + "<br>" + house[i].MESSAGE + "<br><br>"
          }
      }
  })
  return finalmessage
}

// 북봇
async function getBook() {
  let finalBook: string = ""
  let getBook = await createConnection(
    {
      "synchronize": false,
      "logging": false,
      "name" : "Book" ,
      "database": "Book.db",
      "type": "sqlite",
      "entities": [
         "src/entity/Book.ts"
      ],
      "migrations": [
         "src/migration/**/*.ts"
      ],
      "subscribers": [
         "src/subscriber/**/*.ts"
      ],
      "cli": {
         "entitiesDir": "src/entity",
         "migrationsDir": "src/migration",
         "subscribersDir": "src/subscriber"
      }
   }
  )
    .then(async conn => {
      const house = await getConnection("Book")
          .createQueryBuilder()
          .select("BOOK")
          .from(Book, "BOOK")
          .where("BOOK.DATE = :DATE", { DATE: nowdatestr })
          .getMany()
      var data = house[0].CONTENT;
      finalBook = data.replace(/\r/g, "").replace(/\n/g, "<br>");
    })
  return finalBook
}

// 기글봇
async function getGiggle() {
  const axios = require("axios");
  const cheerio = require("cheerio");
  let titleList = [];
  await axios.get("https://gigglehd.com/gg/")
  .then(async html => {
    const $ = cheerio.load(html.data);
    const bodyList = $("tbody tr");
    await bodyList.each(function(i, elem) {
      titleList[i] = "# " + $(elem).find("a:nth-child(2)").text() + "<br>"
    });
  })

  for(var i=0;i<titleList.length;i++){ if(titleList[i] == "# <br>"){ titleList[i] = "" } }
  var data = String(titleList).replace(/,/gi, "") // g:모든 문자열 변경, i:대소문자 무시
  
  return data
}

// 뉴스봇
const parser = new rssParser();
async function getNews() {
    const xml = 'https://news.google.com/rss?gl=KR&hl=ko&ceid=KR:ko';
    const feed = await parser.parseURL(xml);

    let message = '';
    feed.items!.forEach((item) => {
      const { title } = item;
      if (title && item.title.length > 20) {
        message = `${message}<br># ${title}`;
      }
    });
    return message;
}

// 메세지 전송
async function main(finaltitle:string, finalmessage: string) {
  const LeeSooMin = new thecamp.Soldier(
    '이수민',
    '19990103',
    '20200601',
    '예비군인/훈련병',
    '육군',
    '육군훈련소(xx연대)',
    thecamp.SoldierRelationship.FRIEND,
  );
  
  const client = new thecamp.Client();

  await client.login('ID', 'Password');
  await client.addSoldier(LeeSooMin);
 
  const [trainee] = await client.fetchSoldiers(LeeSooMin);
  const message = new thecamp.Message(finaltitle, finalmessage, trainee);
  await client.sendMessage(LeeSooMin, message);
}

// getNews().then(message => { main(month + '월' + day + '일 종합 뉴스', message) })
// getTelegramMessage().then(finalmessage => { main(month + '월' + day + '일 텔레그램 메세지', finalmessage) })
// getGiggle().then(data => { main(month + '월' + day + '일 기글HD', data) })
// getBook().then(finalBook => { main("책읽읍시다 " + nowdate, finalBook) })

getTelegramMessage().then(finalmessage => { console.log(finalmessage + '\n') })
getNews().then(message => { console.log(message + '\n') })
getGiggle().then(data => { console.log(data + '\n') })
getBook().then(finalBook => { console.log(finalBook + '\n') })
