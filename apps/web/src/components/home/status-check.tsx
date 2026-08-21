"use client"

import { useState } from "react"
import type { FormEvent } from "react"
import { FileSearch } from "lucide-react"
import { Card, CardContent } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

export function StatusCheck() {
  const [applicationNumber, setApplicationNumber] = useState("")
  const [message, setMessage] = useState("")
  const [hasError, setHasError] = useState(false)

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()

    if (!applicationNumber.trim()) {
      setHasError(true)
      setMessage("Enter an application number.")
      return
    }

    setHasError(false)
    setMessage(
      "Prototype result: Application received. Next action: Wait for document review."
    )
  }

  return (
    <Card className="h-full">
      <CardContent className="flex h-full flex-col gap-4">
        <div className="flex size-10 shrink-0 items-center justify-center rounded-lg bg-primary/10 text-primary">
          <FileSearch className="size-5" />
        </div>
        <div>
          <h3 className="text-lg font-semibold">Track application</h3>
          <p className="mt-1 text-sm text-muted-foreground">
            Enter the application number to check its current status.
          </p>
        </div>
        <div className="mt-auto">
          <p
            id="application-status-message"
            className={`mb-2 min-h-4 text-xs ${
              hasError ? "text-destructive" : "text-muted-foreground"
            }`}
            aria-live="polite"
          >
            {message}
          </p>
          <form className="flex min-w-0 gap-2" onSubmit={handleSubmit}>
            <Input
              placeholder="Application number"
              aria-label="Application number"
              aria-describedby="application-status-message"
              aria-invalid={hasError}
              autoComplete="off"
              maxLength={40}
              className="h-9 min-w-0 flex-1 text-sm"
              value={applicationNumber}
              onChange={(event) => {
                setApplicationNumber(event.target.value)
                if (hasError) {
                  setHasError(false)
                  setMessage("")
                }
              }}
            />
            <Button
              type="submit"
              size="sm"
              variant="outline"
              className="h-9"
            >
              Check status
            </Button>
          </form>
        </div>
      </CardContent>
    </Card>
  )
}
