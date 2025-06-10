import http from 'k6/http';
import grpc from 'k6/net/grpc';
import {check, sleep} from 'k6';

export let options = {
    vus: 100,
    duration: '10s',
};

// Create and setup gRPC client once
const client = new grpc.Client();
client.load(['/proto'], 'hello.proto');

// The default function runs once per Virtual User(VU) iteration.
// This function is executed repeatedly by each VU during the test duration.
export default function () {
    client.connect('localhost:8081', { plaintext: true });

    const randomId = Math.floor(Math.random() * 20) + 1;

    testRestHello();
    testRestGetProductById(randomId);
    testGrpcInsertProduct();
    testGrpcGetProductById(randomId);

    client.close(); // Each iteration opens and closes a connection immediately
    sleep(1);
}

function testRestHello() {
    const restHelloResponse = http.get('http://localhost:8082/hello');
    const ok = check(restHelloResponse, {
        'REST [/hello] is 200': (r) => r.status === 200
    });
    ok ? console.log("REST test -> [/hello] successful") : console.error("REST test -> [/hello] FAILED");
}

function testRestGetProductById(id) {
    const getProductRestResponse = http.get(`http://localhost:8082/product/get/${id}`);
    const ok = check(getProductRestResponse, {
        'REST [/product/get/{id}] is 200 or 404': (r) => r.status === 200 || r.status === 404
    });
    ok ? console.log("REST test -> [/product/get/{id}] successful") : console.error("REST test -> [/product/get/{id}] FAILED");
}

function testGrpcInsertProduct() {
    const insertProductData = {
        name: `Product_${randomString(5)}`,
        price: String(randomPrice(10.0, 100.0)),
        quantity: Math.floor(Math.random() * 50) + 1,
    };
    const insertGrpcResponse = client.invoke('hello.HelloGrpc/InsertProduct', insertProductData);
    const ok = check(insertGrpcResponse, {
        'gRPC InsertProduct is OK': (r) => r && r.status === grpc.StatusOK
    });
    if (ok && insertGrpcResponse.message) {
        console.log(`gRPC test -> [InsertProduct] Inserted -> { Name: ${insertGrpcResponse.message.name}, Price: ${insertGrpcResponse.message.price}, Qty: ${insertGrpcResponse.message.quantity} }`);
    } else {
        console.error("gRPC test -> [InsertProduct] FAILED");
    }
}

function randomString(length) {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
    return Array.from({ length }, () => chars[Math.floor(Math.random() * chars.length)]).join('');
}

function randomPrice(min, max) {
    return +(Math.random() * (max - min) + min).toFixed(2);
}

function testGrpcGetProductById(id) {
    const getProductGrpcResponse = client.invoke('hello.HelloGrpc/GetProductById', { id: String(id) });
    const ok = check(getProductGrpcResponse, { 'gRPC GetProductById is OK': (r) => r && r.status === grpc.StatusOK });
    if (ok && getProductGrpcResponse.message) {
        console.log(`gRPC test -> [GetProductById] Retrieved -> { Name: ${getProductGrpcResponse.message.name}, Price: ${getProductGrpcResponse.message.price}, Qty: ${getProductGrpcResponse.message.quantity} }`);
    } else {
        console.error("gRPC test -> [GetProductById] FAILED");
    }
}


// The client connection is kept open for all iterations and only closed once after the entire test finishes.
// Difference in CPU usage comes down a lot to when and how you close the client connection.
// export function teardown() {
//     client.close();
// }