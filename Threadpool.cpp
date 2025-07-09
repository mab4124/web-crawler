#include "ThreadPool.h"

ThreadPool::ThreadPool(size_t threads) : stop(false) {
    for (size_t i = 0; i < threads; ++i) {
        workers.emplace_back([this] {
            while (true) {
                std::function<void()> task;
                {
                    std::unique_lock<std::mutex> lock(this->queueMutex);
                    this->condition.wait(lock, [this] {
                        return this->stop || !this->tasks.empty();
                    });
                    if (this->stop && this->tasks.empty())
                        return;
                    task = std::move(this->tasks.front());
                    this->tasks.pop();
                }
                task();
            }
        });
    }
}

void ThreadPool::enqueue(std::function<void()> f) {
    {
        std::unique_lock<std::mutex> lock(queueMutex);
        tasks.push(std::move(f));
    }
    condition.notify_one();
}

void ThreadPool::waitFinished() {
    while (true) {
        std::unique_lock<std::mutex> lock(queueMutex);
        if (tasks.empty()) break;
        lock.unlock();
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
    }
    stop = true;
    condition.notify_all();
    for (std::thread &worker: workers)
        worker.join();
}

ThreadPool::~ThreadPool() {}
