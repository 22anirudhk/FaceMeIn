/**
 * Driver file for this class. To run this file, specify two command-line parameters: the email of the relevant user, 
 * followed by a integer which is 0 if the user is 
 * checking in, 1 if the user is checking out, and 2 if the user is being removed.
 * A third optional parameter is the millisecond time when the user will be added; otherwise, 
 * the current time will be used for any of the three operations. Removal requires the date (but not time) to match.
 */
const mongoose = require("./db");
const Entry = require("./entry") // entry.js required
Entry.find({}).then((attendanceData) => main(attendanceData))

/**
 * The driver function for testing this code.
 * @param {*} attendanceData 
 */
function main(attendanceData)
{
   var email = process.argv[2].toLowerCase() // command-line parameters begin at index 2
   var operation = parseInt(process.argv[3]) 
   var time = process.argv[4] === undefined ? getCurrentTime() : parseInt(process.argv[4])

   var attendanceObj = getAttendanceObj(email, time, attendanceData)
   if (operation == 0)
   {
      if (attendanceObj != null && attendanceObj.checkOut == null) // already checked in before and didn't check out
      {
         console.log("You're already checked in.")
         mongoose.connection.close()
         console.log(1)
      }
      else
      {
         attendanceObj = createAttendanceObj(email, time)
         Entry.create(attendanceObj).then(() => mongoose.connection.close())
         console.log("Checked in!")
         console.log(0)
      }
   }
   else if (operation == 1)
   {
      if (attendanceObj == null) // not yet checked in
      {
         console.log("You're not yet checked in.")
         mongoose.connection.close()
         console.log(1)
      }
      else 
      {
         attendanceObj.checkOut = time
         Entry.findByIdAndUpdate(attendanceObj._id, attendanceObj, {upsert: true}, function(err, res) {}).then(() => mongoose.connection.close())
         console.log("Checked out!")
         console.log(0)
      }
   }
   else if (operation == 2)
   {
      if (attendanceObj == null)
      {
         console.log("No matching entry. Nothing was removed.")
      }
      else
      {
         Entry.deleteOne({_id: attendanceObj._id}).exec().then(() => mongoose.connection.close())
         console.log("Your entry has been removed.")
         console.log(0)
      }
   }
}

/**
 * Generates an attendance object corresponding to a given email, check-in time, and optional check-out time.
 * 
 * @param {*} email 
 * @param {*} checkIn 
 * @param {*} checkOut 
 */
function createAttendanceObj(email, checkIn, checkOut = null)
{
   return {email: email, checkIn: checkIn, checkOut: checkOut}
}

/**
 * Retrieves a date object corresponding to the current time.
 */
function getCurrentTime()
{
   return new Date().getTime()
}

/**
 * Retrieves the attendance object out of a given dataset with an email and day corresponding 
 * to a given email.
 * 
 * @param {*} email 
 * @param {*} day 
 * @param {*} attendanceData 
 */
function getAttendanceObj(email, day, attendanceData)
{
   var date = new Date(day)
   for (var i = 0; i < attendanceData.length; i++)
   {
      dataVal = new Date(attendanceData[i].checkIn)
      
      if (attendanceData[i].email == email && dataVal.getFullYear() == date.getFullYear() && dataVal.getMonth() == date.getMonth() && 
          dataVal.getDate() == date.getDate())
      {
         return attendanceData[i]
      }
   }

   return null
}