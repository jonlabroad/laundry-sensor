import { CloudWatch, SNS } from "aws-sdk";

'use strict';

interface StatusData {
  status: string
}

interface AlarmData {
  waterStatus: string
}

interface PostInput {
  type: "STATUS" | "WATER_DETECTED" | "RESET" | "LAUNDRY_START" | "LAUNDRY_END"
  test: boolean
}

const snsArn = "arn:aws:sns:us-east-1:796987500533:WaterEventSMS";

export const detect = async (event, context, callback) => {
  try {
    let response = {};
    console.log(event);
    const eventDataRaw = JSON.parse(event.body) as PostInput;

    if (eventDataRaw.type === "STATUS") {
      const params = {
        MetricData: [
          {
            MetricName: "Status",
            Timestamp: new Date(),
            Value: 1,
            Dimensions: [
              {
                Name: "test",
                Value: eventDataRaw.test ? "1" : "0",
              }
            ]
          }
        ],
        Namespace: "LaundryWaterSensor1"
      };
      const cloudwatch = new CloudWatch();
      response = await cloudwatch.putMetricData(params).promise();
    } else if (eventDataRaw.type === "WATER_DETECTED") {
      const params = {
        MetricData: [
          {
            MetricName: "WaterDetected",
            Timestamp: new Date(),
            Value: 1,
            Dimensions: [
              {
                Name: "test",
                Value: eventDataRaw.test ? "1" : "0",
              }
            ]
          }
        ],
        Namespace: "LaundryWaterSensor1"
      };
      const cloudwatch = new CloudWatch();
      response = await cloudwatch.putMetricData(params).promise();
    } else if (eventDataRaw.type === "LAUNDRY_START") {
      const params = {
        MetricData: [
          {
            MetricName: "LaundryStart",
            Timestamp: new Date(),
            Value: 1,
            Dimensions: [
              {
                Name: "test",
                Value: eventDataRaw.test ? "1" : "0",
              }
            ]
          }
        ],
        Namespace: "LaundryWaterSensor1"
      };
      const cloudwatch = new CloudWatch();
      response = await cloudwatch.putMetricData(params).promise();
      if (!eventDataRaw.test) {
        const sns = new SNS();
        await sns.publish({
          TopicArn: snsArn,
          Message: `Water Detected: ${new Date().toISOString()}.\nTest=${eventDataRaw.test}`
        }).promise();
      }
    } else if (eventDataRaw.type === "LAUNDRY_END") {
      const params = {
        MetricData: [
          {
            MetricName: "LaundryEnd",
            Timestamp: new Date(),
            Value: 1,
            Dimensions: [
              {
                Name: "test",
                Value: eventDataRaw.test ? "1" : "0",
              }
            ]
          }
        ],
        Namespace: "LaundryWaterSensor1"
      };
      const cloudwatch = new CloudWatch();
      response = await cloudwatch.putMetricData(params).promise();
    }
  } catch (err) {
    console.error(err);
    return {
      statusCode: 500,
      body: err.message,
    };
  }

  console.log("HERE?");
  return {
    statusCode: 200,
    body: "",
  };

  // Use this code if you don't use the http event with the LAMBDA-PROXY integration
  //return { message: 'Go Serverless v1.0! Your function executed successfully!', event };
};
